#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'pymongo',
    'requests',
    'scipy',
    'colorlog',
    'etaprogress',
]

setup(
    version='0.1',
    description='ACBBS Python libraries',
    name = "acbbs",
    author="Hardware Team",
    author_email = "hardware@sigfox.com",
    license='Other/Proprietary License',
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    packages = find_packages()
)
