# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import picrawler

setup(
    name='picrawler',
    version=picrawler.__version__,
    description='A distributed web crawler using PiCloud.',
    author='Ikuya Yamada',
    author_email='ikuya@ousia.jp',
    packages=find_packages(),
    install_requires=[
        'cloud>=2.8',
        'requests',
    ],
    tests_require=[
        'nose',
        'mock',
    ],
    test_suite = 'nose.collector'
)
