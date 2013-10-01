# -*- coding: utf-8 -*-

import cloud


class RTCoreRequest(object):
    """A wrapper class that requests real-time cores to PiCloud.

    Usage:
        >>> from picrawler.rt_cores import RTCoreRequest
        >>> with RTCoreRequest(core_type='s1', num_cores=10):
        ...     pass

    :param str core_type: The PiCloud core type.
    :param int num_cores: The number of cores.
    :param int max_duration: (optional) The lifetime of the request, in hours.
    """

    def __init__(self, core_type, num_cores, max_duration=None):
        self._core_type = core_type
        self._num_cores = num_cores
        self._max_duration = max_duration

    def __enter__(self):
        self._request_id = self.request()

        return self

    def __exit__(self, type, value, traceback):
        self.release(self._request_id)

    def request(self):
        """Requests PiCloud's realtime cores.

        :return: Request ID
        """

        req = cloud.realtime.request(self._core_type, self._num_cores,
                                     self._max_duration)
        req_id = req['request_id']

        return req_id

    def release(self, req_id):
        """Releases PiCloud's realtime cores.

        :param int req_id: The request ID.
        """

        cloud.realtime.release(req_id)
