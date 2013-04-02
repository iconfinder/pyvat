#!/usr/bin/env python
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'pyvat',
]

requires = [
    'requests>=1.0.0,<2.0.0',
]

tests_require = [
    'nose',
    'rednose',
    'pep8',
]

setup(
    name='pyvat',
    version='1.0.0',
    description='VAT validation for Python',
    author='Nick Bruun',
    author_email='nick@bruun.co',
    url='http://bruun.co/',
    packages=packages,
    package_dir={'pyvat': 'pyvat'},
    include_package_data=True,
    tests_require=tests_require,
    install_requires=requires,
    #license=open('LICENSE').read(),
    zip_safe=True,
)
