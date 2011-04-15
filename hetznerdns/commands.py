import cli.app
import time
import service

class BaseApp(cli.app.CommandLineApp):
    def __init__(self, *args, **kwargs):
        super(BaseApp, self).__init__(*args, **kwargs)
        self.add_param('-u', '--user', default='')
        self.add_param('-p', '--password', default='')
        
class AddApp(BaseApp):
    def __init__(self, *args, **kwargs):
        super(AddApp, self).__init__(*args, **kwargs)
        self.add_param('-t', '--type', default='standard')
        self.add_param('-d', '--domain')
        self.add_param('-i', '--ip')

class ListApp(BaseApp):
    pass

class DeleteApp(BaseApp):
    def __init__(self, *args, **kwargs):
        super(DeleteApp, self).__init__(*args, **kwargs)
        self.add_param('-d', '--domain')

def _get_domain_id(client, domain):
    domain_map = dict(client.list())
    domain_inv_map= dict((v,k) for k, v in domain_map.iteritems())
    return domain_map[domain_id] if domain.isdigit() else domain_inv_map[domain]
    
@AddApp
def command_add(app):
    print "Adding domain %s" % app.params.domain
    user, password = app.params.user, app.params.password
    client = service.HetznerDns(user, password)
    client.login()
    client.add(app.params.domain, app.params.type, app.params.ip)

@ListApp
def command_list(app):
    print "List of domains:"
    user, password = app.params.user, app.params.password
    client = service.HetznerDns(user, password)
    client.login()
    for domain_data in client.list():
        print ', '.join(domain_data)

@DeleteApp
def command_delete(app):
    user, password = app.params.user, app.params.password
    client = service.HetznerDns(user, password)
    client.login()
    domain = app.params.domain
    domain_id = _get_domain_id(client, domain)
    print "Removing domain=%s, id=%s" % (domain, domain_id)
    client.delete(domain_id)
    

