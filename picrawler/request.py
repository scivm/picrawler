# -*- coding: utf-8 -*-

import uuid
import requests

from response import Response, ErrorResponse

_success_callbacks = {}
_error_callbacks = {}

SUPPORTED_HTTP_METHODS = frozenset(['get', 'post', 'put', 'delete', 'head', 'options'])


class InvalidHTTPMethod(Exception):
    pass


class InvalidResponse(Exception):
    pass


class Request(object):
    """Class that represents a request to PiCloud.

    :param str url: A URL to be fetched.
    :param str method: Target HTTP method.
        ("GET" or "POST" or "PUT" or "DELETE" or "HEAD" or "OPTIONS")
    :param dict headers: HTTP headers to send. (Default: {})
    :param dict args: Additional arguments, that are directly passed to
        `requests <http://docs.python-requests.org>`_. Any arguments that supported in `requests <http://docs.python-requests.org>`_ are supported.
    :param function success_callback: A function called if the request is
        successfully completed. A :class:`Response <picrawler.response.Response>`
        instance is passed as the first argument.
    :param function error_callback: A function called if the request is failed.
        An :class:`ErrorResponse <picrawler.response.ErrorResponse>` instance is passed as the first argument.
    """

    def __init__(self, url, method='get', headers={}, args={},
                 success_callback=None, error_callback=None):
        global _success_callbacks, _error_callbacks

        self._id = uuid.uuid1().hex
        self._url = url
        self._method = method.lower()
        self._headers = headers
        self._args = args
        self._success_callback_id = None
        self._error_callback_id = None

        if not self._method in SUPPORTED_HTTP_METHODS:
            raise InvalidHTTPMethod('Unsupported HTTP method')

        # NOTE: because the callback function cannot be pickled,
        # it must be saved locally
        if success_callback:
            self._success_callback_id = uuid.uuid1().hex
            _success_callbacks[self._success_callback_id] = success_callback

        if error_callback:
            self._error_callback_id = uuid.uuid1().hex
            _error_callbacks[self._error_callback_id] = error_callback

    @property
    def id(self):
        return self._id

    def run_callback(self, response):
        global _success_callbacks, _error_callbacks

        if isinstance(response, Response):
            if self._success_callback_id:
                _success_callbacks[self._success_callback_id](response)
        elif isinstance(response, ErrorResponse):
            if self._error_callback_id:
                _error_callbacks[self._error_callback_id](response)
        else:
            raise InvalidResponse('Invalid response')

    def __call__(self):
        method_func = getattr(requests, self._method)

        try:
            ret = method_func(self._url, headers=self._headers, **self._args)
        except Exception, e:
            return ErrorResponse(self, e)

        return Response(self, ret.status_code, ret.content, ret.headers)
