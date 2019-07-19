#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'pymongo',
    'requests',
    'scipy',
    'colorlog',
    'etaprogress',
    'pyModbusTCP',
    'acbbs==2.0.2',
    'aioredis==1.2.0',
    'asgiref==3.1.2',
    'asn1crypto==0.24.0',
    'async-timeout==2.0.1',
    'asyncio==3.4.3',
    'attrs==19.1.0',
    'autobahn==19.6.2',
    'Automat==0.7.0',
    'backcall==0.1.0',
    'certifi==2019.3.9',
    'cffi==1.12.3',
    'channels==2.2.0',
    'channels-redis==2.3.2',
    'chardet==3.0.4',
    'colorlog==4.0.2',
    'constantly==15.1.0',
    'cryptography==2.7',
    'daphne==2.3.0',
    'decorator==4.4.0',
    'Django==2.0',
    'django-bootstrap3==11.0.0',
    'etaprogress==1.1.1',
    #'gpib==1.0',
    'hiredis==1.0.0',
    'hyperlink==19.0.0',
    'idna==2.8',
    'incremental==17.5.0',
    'ipython==6.5.0',
    'ipython-genutils==0.2.0',
    'jedi==0.13.3',
    'jsonfield==2.0.2',
    'mod-wsgi==4.6.5',
    'msgpack==0.5.6',
    'numpy==1.16.3',
    'parso==0.4.0',
    'pexpect==4.7.0',
    'pickleshare==0.7.5',
    'prompt-toolkit==1.0.16',
    'ptyprocess==0.6.0',
    'pycparser==2.19',
    'Pygments==2.3.1',
    'PyHamcrest==1.9.0',
    'pyModbusTCP==0.1.8',
    'pymongo==3.8.0',
    'pytz==2019.1',
    'redis==2.10.6',
    'requests==2.21.0',
    'scipy==1.2.1',
    'simplegeneric==0.8.1',
    'six==1.12.0',
    'traitlets==4.3.2',
    'Twisted==19.2.1',
    'txaio==18.8.1',
    'typing==3.6.6',
    'urllib3==1.24.2',
    'wcwidth==0.1.7',
    'zope.interface==4.6.0',

]

with open('acbbs/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)                        
if not version:
    raise RuntimeError('Cannot find version information')

with open('acbbs/__init__.py', 'r') as fd:
    confpath = re.search(r'^__confpath__\s*=\s*[\'"]([^\'"]*)[\'"]',
                         fd.read(), re.MULTILINE).group(1)                        
if not confpath:
    raise RuntimeError('Cannot find confpath')

if not os.path.exists(confpath):
    os.system("mkdir %s" % confpath)
    os.system("chown $(whoami):$(whoami) %s" % confpath)
if not os.path.exists(confpath + "/configuration.json"):
    os.system("cp conf/configuration.json %s/" % confpath)
if not os.path.exists(confpath + "/swtch_cal.json"):
    os.system("cp conf/swtch_cal.json %s/" % confpath)

os.system("cp acbbs-scheduler.py acbbs-config.py acbbs-calibration.py /etc/acbbs")
os.system("ln -s /etc/acbbs/acbbs-scheduler.py /usr/bin/acbbs-scheduler")
os.system("ln -s /etc/acbbs/acbbs-config.py /usr/bin/acbbs-config")
os.system("ln -s /etc/acbbs/acbbs-calibration.py /usr/bin/acbbs-calibration")

setup(
    version=version,
    description='ACBBS Python libraries',
    name = "acbbs",
    author="Hardware Team",
    author_email = "hardware@sigfox.com",
    license='Other/Proprietary License',
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    #data_files = [('', ['acbbs/configuration.json'])],
    package_data={'': ['drivers/toolIQ']},
    packages = find_packages()
)
