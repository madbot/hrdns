from setuptools import setup, find_packages

setup(
    name= "HetznerDns",
    version=  "dev",
    packages= find_packages(),
    install_requires= ['pyquery',],
    scripts= ['hetznerdns/hetznerdns.py',],
    author= 'Jarek S.',
    author_email= 'jarekps@sysd.pl',
    description= 'Small tool created for management of hetzner dns service from commandline',
    license= 'Beerware/BSD',
    keywords= 'hetzner dns management commandline pycli',
    url= 'http://hetznerdns.sysd.pl',
)