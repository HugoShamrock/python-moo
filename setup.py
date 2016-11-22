#!/usr/bin/env python3

from setuptools import setup

import moo

long_description = open('README.rst').read() + '\n' + open('CHANGES.rst').read()

setup(
    name='python-moo',
    version=moo.__version__,
    description='Easy way how to run the same query in multiple SQL databases',
    long_description=long_description,
    author='Hugo Shamrock',
    author_email='hugo.shamrock@gmail.com',
    url='https://github.com/HugoShamrock/python-moo',
    packages=['moo'],
    classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Database',
        'Topic :: Software Development',
        'Topic :: System',
    ],
)
