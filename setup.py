#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools


packages = ['']
requires = ['pyaml']

setuptools.setup(
    name='nntp-indexer',
    version='0.1',
    description='Usenet indexer.',
    author='Fabien Reboia',
    author_email='srounet@gmail.com',
    packages=setuptools.find_packages(),
    include_package_data=True,
    test_suite='tests',
    install_requires=requires,
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
