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
    os.system("sudo mkdir %s" % confpath)
    os.system("sudo chown $(whoami):$(whoami) %s" % confpath)
if not os.path.exists(confpath + "/configuration.json"):
    os.system("cp conf/configuration.json %s/" % confpath)

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
