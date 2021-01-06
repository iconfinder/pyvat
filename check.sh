#!/bin/bash

rm -rfv dist/*
python setup.py sdist
python setup.py bdist_wheel --universal
twine check dist/*


