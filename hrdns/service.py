import os
import cookielib
import urllib2
import urllib
from pyquery import PyQuery as pq

class HDInvalidLoginData(Exception): pass
class HDInvalidDomainAdd(Exception): pass
class HDInvalidDomainDelete(Exception): pass
class HDInvalidDomainShow(Exception): pass
class HDInvalidDomainUpdate(Exception): pass
class HDDomainNotFound(Exception): pass

class HetznerDns(object):
    login_url = 'https://robot.your-server.de/login/check'
    base_url = 'https://robot.your-server.de'
    
    def __init__(self, user, password):
        self.user = user
        self.password = password
        cookiejar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        self.opener = opener
        
    def _request(self, url, data=None):
        if data:
            data = urllib.urlencode(data)
        if url.find(self.base_url) == -1:
            url = self.base_url + url
        return self.opener.open(url, data)
        
    def login(self):
        self._request('/')
        params = dict(user=self.user, password=self.password)        
        request = self._request(self.login_url, params)
        data = request.read()
        
        if data.find('Welcome to your webinterface for server and domain administration.') != -1:
            return
        else:
            document = pq(data)
            error_p = document(".startpage_error")
            error = error_p[0].text if error_p else 'Undefined Error'
        raise HDInvalidLoginData(error)
    
    def add(self, domain, domain_type, ip):
        params = dict(domain=domain, type=domain_type, ip=ip)
        request = self._request("/dns/data", params)
        data = request.read()
        if data.find('Thank you for your order.') != -1:
            return            
        document = pq(data)
        errors = []
        for error in document('.error_list li'):
            i = [ x for x in error.getparent().getparent().getchildren() if x.tag.lower()=='input' ][0]
            errors.append("%s: %s" % (i.attrib['name'], error.text))
        raise HDInvalidDomainAdd(os.linesep.join(errors))

    def list(self):
        domains = []
        request = self._request('/dns/index/page/1')
        document = pq(request.read())
        pageli = document('ul.box_page li')
        pages = ['1',]
        for li in pageli:
            if isinstance(li.text, basestring) and li.text.isdigit():
                pages.append(li.text)
        pages = list(set(pages))
        for page in pages: 
           domains.extend(self.get_page(page))
        return domains

    def get_page(self, page):
        domains = []
        request = self._request('/dns/index/page/%s' % page)
        document = pq(request.read())
        divs = document("div[id^='data_']")
        for div in divs:
            domains.append([div.attrib['id'].split('_')[1],])
        tds = document('td.title')
        for i,td in enumerate(tds[1:]):
            domains[i].append(td.text)
        return domains
        
    def delete(self, domain_id):
        request_data = self._request('/dns/delete', dict(delete='true', id=domain_id)).read()
        if request_data.find('Thank you for your order. The DNS entry will now be deleted.') != -1:
            return
        raise HDInvalidDomainDelete

    
    def get_entries(self, domain_id):
        request = self._request('/dns/update/id/%s/' % domain_id, {'v':1})
        document = pq(request.read())
        zonefile = document("textarea[name=zonefile]")
        if zonefile:
            return zonefile.html()
        raise HDInvalidDomainShow
        

    def update_entries(self, domain_id, entries):
        request = self._request('/dns/update/', dict(id=domain_id, zonefile=entries))
        data = request.read()
        if data.find('Thank you for your order. The DNS entry will be updated now.') != -1:
            return
        document = pq(data)
        errors = []
        for error in document('.error_list li'):
            errors.append(error.text)
        raise HDInvalidDomainUpdate(os.linesep.join(errors))
    
    def get_domain_id(self, domain):
        domain_map = dict(self.list())
        domain_inv_map= dict((v,k) for k, v in domain_map.iteritems())
        try:
            return domain_map[domain] if domain.isdigit() else domain_inv_map[domain]
        except KeyError:
            raise HDDomainNotFound("Domain %s doesn't exist on hetzner dns." % domain)
        
