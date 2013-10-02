PiCrawler
=========

.. image:: https://travis-ci.org/studio-ousia/picrawler.png?branch=master
    :target: https://travis-ci.org/studio-ousia/picrawler

PiCrawler is a distributed web crawler using PiCloud.


.. code-block:: python

    >>> from picrawler import PiCloudConnection
    >>>
    >>> with PiCloudConnection() as conn:
    ...     response = conn.send(['http://www.wikipedia.org'])
    ...     print 'status code:', response[0].status_code
    ...     print 'content:', response[0].content[:15]
    status code: 200
    content: <!DOCTYPE html>


Installation
------------

To install picrawler, simply:

.. code-block:: bash

    $ pip install picrawler


Documentation
-------------

Documentation is available at http://picrawler.readthedocs.org/.
