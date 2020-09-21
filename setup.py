#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


packages = [
    'pyvat',
]

requires = [
    'requests>=1.0.0,<3.0',
    'pycountry',
    'enum34',
]

tests_require = [
    'nose',
    'rednose',
    'flake8',
    'unittest2',
]

setup(
    name='pyvat',
    version='1.3.5',
    description='VAT validation for Python',
    author='Iconfinder',
    author_email='support@iconfinder.com',
    url='http://www.iconfinder.com',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'pyvat': 'pyvat'},
    include_package_data=True,
    tests_require=tests_require,
    install_requires=requires,
    license=open('LICENSE').read(),
    zip_safe=True,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
    ),
)
