# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='picrawler',
    version='0.1',
    description='A distributed web crawler using PiCloud.',
    author='Studio Ousia',
    author_email='admin@ousia.jp',
    url='http://github.com/studio-ousia/picrawler',
    packages=find_packages(),
    license=open('LICENSE').read(),
    include_package_data=True,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
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
