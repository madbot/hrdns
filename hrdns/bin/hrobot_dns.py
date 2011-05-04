#!/usr/bin/env python
import sys
import hrdns.commands
import time

allowed_modules = ('add', 'show', 'update', 'delete', 'list')

if __name__ == '__main__':    
    if len(sys.argv) >= 2:
        module_name = sys.argv[1]
        if module_name in allowed_modules:
            sys.argv.pop(1)
            app = getattr(hrdns.commands, 'command_%s' % module_name)
            app.run()
        else:
            print "Not found module called %s. Choose from %s." % (module_name, ', '.join(allowed_modules))
            sys.exit(-1)
    print "Select module from list and call: hrobot_dns.py <module_name> --params"
    print "Available modules: %s" % ', '.join(allowed_modules)
    print "Read https://github.com/jareks/hrdns/blob/master/README"
    sys.exit(-1)