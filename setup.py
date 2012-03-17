from setuptools import setup, find_packages

setup(
    name= "hrdns",
    version= "dev",
    packages= find_packages(),
    install_requires= ['pyquery', 'pyCli'],
    scripts= ['hrdns/bin/hrobot_dns.py',],
    author= 'Jarek S.',
    author_email= 'jarekps@sysd.pl',
    description= 'Small tool created for management of hetzner dns service from commandline',
    license= 'X11',
    keywords= 'hetzner dns management commandline pycli',
    url= 'http://github.com/jareks/hrdns',
)
