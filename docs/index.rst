.. picrawler documentation master file, created by
   sphinx-quickstart on Mon Sep 30 21:15:12 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to picrawler's documentation!
=====================================

PiCrawler is a distributed web crawler using PiCloud.

Using PiCrawler, you can easily implement a distributed web crawler within a few lines of code.

.. code-block:: python

    >>> from picrawler import PiCloudConnection
    >>>
    >>> with PiCloudConnection() as conn:
    ...     response = conn.send(['http://en.wikipedia.org/wiki/Star_Wars',
    ...                           'http://en.wikipedia.org/wiki/Darth_Vader'])
    ...     print 'status code:', response[0].status_code
    ...     print 'content:', response[0].content[:15]
    status code: 200
    content: <!DOCTYPE html>


Contents:

.. toctree::
   :maxdepth: 2

   install
   getting_started
   api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

