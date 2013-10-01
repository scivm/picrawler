# -*- coding: utf-8 -*-

import cPickle as pickle
import zlib


class BaseResponse(object):
    def __init__(self, request):
        self._request = request

    @property
    def request(self):
        return self._request

    def run_callback(self):
        self._request.run_callback(self)

    # override __getstate__ and __setstate__ to reduce the size of a pickled
    # instance by compressing instance attributes using zlib
    def __getstate__(self):
        pickled_dict = pickle.dumps(self.__dict__, protocol=2)
        return zlib.compress(pickled_dict, 9)

    def __setstate__(self, state):
        pickled_dict = zlib.decompress(state)
        self.__dict__ = pickle.loads(pickled_dict)


class Response(BaseResponse):
    """Class that represents a response from PiCloud."""

    def __init__(self, request, status_code, content, headers):
        super(Response, self).__init__(request)

        self._status_code = status_code
        self._headers = headers
        self._content = content

    @property
    def status_code(self):
        """HTTP status code.

        :type: int
        """
        return self._status_code

    @property
    def content(self):
        """HTTP content.

        :type: str
        """
        return self._content

    @property
    def headers(self):
        """HTTP headers.

        :type: dict
        """
        return self._headers


class ErrorResponse(BaseResponse):
    """Class that represents a runtime error occurred on running the job."""

    def __init__(self, request, exception):
        super(ErrorResponse, self).__init__(request)

        self._exception = exception

    @property
    def exception(self):
        """Exception raised in the runtime.

        :type: :class:`Exception`
        """
        return self._exception
