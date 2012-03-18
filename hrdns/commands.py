import cli.app
import time
import ConfigParser
import service
import os
import sys

class BaseApp(cli.app.CommandLineApp):
    def __init__(self, *args, **kwargs):
        super(BaseApp, self).__init__(*args, **kwargs)
        self.add_param('-u', '--user', default='')
        self.add_param('-p', '--password', default='')
        config_path = os.path.join(os.getenv('HOME'), '.hrdnsrc')
        try:
            self.conf = ConfigParser.ConfigParser()
            self.conf.readfp(open(config_path, 'rU+'))
        except IOError:
            self.conf = None
        except ConfigParser.Error,e:
            self.conf = None
            print "Your config couldn't be parsed because:", e
        
    def pre_run(self, *args, **kwargs):
        super(BaseApp, self).pre_run(*args, **kwargs)
        try:
            user = os.getenv('HRDNS_USER', None) or (self.conf.get('hrdns', 'user', None)\
                    if self.conf else None) or self.params.user
        except ConfigParser.Error,e:
            print "Your config file is broken, cannot get user:",e
            user = self.params.user

        try:
            password = os.getenv('HRDNS_PASSWORD', None) or (self.conf.get('hrdns', 'password', None)\
                        if self.conf else None) or self.params.password
        except ConfigParser.Error,e:
            print "Your config file is broken, cannot get password", e
            password = self.params.password
        self.client = service.HetznerDns(user, password)
        self.client.login()        

class AddApp(BaseApp):
    def __init__(self, *args, **kwargs):
        super(AddApp, self).__init__(*args, **kwargs)
        self.add_param('-t', '--type', default='standard')
        self.add_param('-d', '--domain')
        self.add_param('-i', '--ip')

class ListApp(BaseApp):
    pass

class WithDomainApp(BaseApp):
    def __init__(self, *args, **kwargs):
        super(WithDomainApp, self).__init__(*args, **kwargs)
        self.add_param('-d', '--domain')

    def pre_run(self):
        super(WithDomainApp, self).pre_run()
        self.domain = self.params.domain
        self.domain_id = self.client.get_domain_id(self.domain)

class UpdateEntryApp(WithDomainApp):
    def __init__(self, *args, **kwargs):
        super(UpdateEntryApp, self).__init__(*args, **kwargs)
        self.add_param('-f', '--file')
        
@AddApp
def command_add(app):
    print "Adding domain %s" % app.params.domain
    app.client.add(app.params.domain, app.params.type, app.params.ip)

@ListApp
def command_list(app):
    print "List of domains:"
    for domain_data in app.client.list():
        print ', '.join(domain_data)

@WithDomainApp
def command_delete(app):
    print "Removing domain=%s, id=%s" % (app.domain, app.domain_id)
    app.client.delete(app.domain_id)
    
@WithDomainApp
def command_show(app):
    entries = app.client.get_entries(app.domain_id)
    sys.stdout.write(entries)

@UpdateEntryApp
def command_update(app):
    print "Updating entries domain=%s, id=%s" % (app.domain, app.domain_id)
    with open(app.params.file, "r+") as zonefile:
        contents = zonefile.read()
        app.client.update_entries(app.domain_id, contents)
