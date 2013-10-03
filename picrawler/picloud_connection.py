# -*- coding: utf-8 -*-

import cloud
import collections
import datetime

from request import Request

REQUEST_QUEUE_PREFIX = 'picrawler_request_'
RESULT_QUEUE_PREFIX = 'picrawler_result_'


class InvalidRequest(Exception):
    pass


class PiCloudConnection(object):
    """Class that represents a connection to PiCloud.

    Usage:

        >>> from picrawler import PiCloudConnection
        >>> with PiCloudConnection() as conn:
        ...     response = conn.send(['http://www.wikipedia.org'])
        ...     print 'status code:', response[0].status_code
        ...     print 'content:', response[0].content[:15]
        status code: 200
        content: <!DOCTYPE html>

    :param int max_parallel_jobs: (optional) The number of parallel jobs to run.
    :param str core_type: (optional) PiCloud core type.
    """

    def __init__(self, max_parallel_jobs=10, core_type='s1'):
        self._max_parallel_jobs = max_parallel_jobs
        self._core_type = core_type

        self._connected = False

    def __enter__(self):
        if not self._connected:
            self.connect()

        return self

    def __exit__(self, type, value, traceback):
        self.close()

    @property
    def is_connected(self):
        return self._connected

    @property
    def request_queue(self):
        return self._request_queue

    @property
    def result_queue(self):
        return self._result_queue

    def connect(self):
        """Establishes a connection to PiCloud."""

        self._initialize_queues()

        self._connected = True

    def close(self):
        """Closes the connection."""

        assert self._connected, 'The connection to PiCloud has not been established.'

        self._destroy_queues()
        cloud.close()

        self._connected = False

    def send(self, req):
        """Sends the requests to PiCloud.

        :param req: Requests to be sended to PiCloud. Must be one of the following:

            * A string that contains a URL
            * A list or a tuple or an iteratable that consists of URL strings
            * A :class:`Request <picrawler.request.Request>` instance
            * An list or a tuple or an iteratable that consists of :class:`Request <picrawler.request.Request>` instance

        :return: List of :class:`BaseResponse <picrawler.response.BaseResponse>` instances.
        """

        assert self._connected, 'The connection to PiCloud has not been established.'

        # covert req into a list of Request instances
        if isinstance(req, basestring):
            requests = [Request(req)]

        elif isinstance(req, Request):
            requests = [req]

        elif isinstance(req, collections.Iterable):
            requests = []
            for request in req:
                if isinstance(request, Request):
                    requests.append(request)
                elif isinstance(request, basestring):
                    requests.append(Request(request))
                else:
                    raise InvalidRequest('Invalid request item')

        else:
            raise InvalidRequest('req must be either an instance of the '
                                 'Request class or an iteratable of Request instances')

        # send requests to the PiCloud queue
        self._request_queue.push(requests)

        responses = self._loop()
        req_resp_map = {}
        for resp in responses:
            req_resp_map[resp.request.id] = resp

        return [req_resp_map.get(r.id) for r in requests]

    def _initialize_queues(self):

        queue_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self._request_queue = cloud.queue.get(REQUEST_QUEUE_PREFIX + queue_id)
        self._result_queue = cloud.queue.get(RESULT_QUEUE_PREFIX + queue_id)

        # attach the request handler to the queue
        self._request_queue.attach(lambda req: req(),
                                   output_queues=[self._result_queue],
                                   max_parallel_jobs=self._max_parallel_jobs,
                                   _type=self._core_type)

    def _destroy_queues(self):

        self._request_queue.delete()
        self._result_queue.delete()

        self._request_queue = None
        self._result_queue = None

    def _loop(self):
        gathered_responses = []

        c = 0
        while True:
            # get the results
            responses = self._result_queue.pop(timeout=0)

            if responses:
                for response in responses:
                    response.run_callback()

                gathered_responses += responses

            # break the loop if completed
            if c % 10 == 0 and self._requests_completed():
                break

            c += 1

        return gathered_responses

    def _requests_completed(self):
        request_queue_info = self._request_queue.info()

        if (request_queue_info['count'] == 0 and
            request_queue_info['processing_jobs'] == 0 and
            request_queue_info['queued_jobs'] == 0):

            # exit the loop if the result queue is empty
            if self._result_queue.count() == 0:
                return True

        return False
