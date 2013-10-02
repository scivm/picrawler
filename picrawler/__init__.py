# -*- coding: utf-8 -*-

"""
PiCrawler
~~~~~~~~~

PiCrawler is a distributed web crawler using PiCloud.

Usage:

    >>> from picrawler import PiCloudConnection
    >>> with PiCloudConnection() as conn:
    ...     response = conn.send(['http://www.wikipedia.org'])
    ...     print 'status code:', response[0].status_code
    ...     print 'content:', response[0].content[:15]
    status code: 200
    content: <!DOCTYPE html>

:copyright: (c) 2013 by Studio Ousia.
:license: Apache 2.0, see LICENSE for more details.

"""

__title__ = 'picrawler'
__version__ = '0.0.1'
__author__ = 'Studio Ousia'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2013 Studio Ousia'


from picloud_connection import PiCloudConnection
from request import Request
