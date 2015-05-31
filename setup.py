#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='fabric-web-worker',
    version='dev',
    packages=['libs', 'test'],
    url='https://github.com/zhwei/fabric-web-worker',
    install_requires=[
        'Flask>=0.10.1',
        'Fabric>=1.10.1',
        'tailer==0.3',
    ],
    license='',
    author='zhwei',
    author_email='zhwei.yes@gmail.com',
    description='Fabric Web Worker.'
)
