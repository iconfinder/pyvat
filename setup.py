#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

packages = [
    'pyvat',
]

requires = [
    'requests>=1.0.0,<3.0',
    'pycountry'
]

tests_require = [
    'nose',
    'rednose',
    'flake8'
]

setup(
    name='pyvat',
    version='1.3.18',
    description='VAT validation for Python',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author='Iconfinder',
    author_email='support@iconfinder.com',
    url='https://www.iconfinder.com',
    project_urls={
        'Issue Tracker': 'https://github.com/iconfinder/pyvat/issues',
    },
    packages=packages,
    install_requires=requires,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ),
)
