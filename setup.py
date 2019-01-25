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
