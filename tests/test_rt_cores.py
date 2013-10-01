# -*- coding: utf-8 -*-

from nose.tools import *
from mock import patch

from picrawler.rt_cores import RTCoreRequest


class TestRTCoreRequest(object):
    @patch('picrawler.rt_cores.cloud')
    def test_request(self, mock_cloud):
        req = RTCoreRequest('c1', 10, 1)

        mock_cloud.realtime.request.return_value = dict(request_id=10)

        req_id = req.request()

        mock_cloud.realtime.request.assert_called_once_with('c1', 10, 1)
        eq_(10, req_id)

    @patch('picrawler.rt_cores.cloud')
    def test_release_rt_cores(self, mock_cloud):
        req = RTCoreRequest('c1', 10, 1)

        mock_cloud.realtime.request.return_value = dict(request_id=10)

        req_id = req.request()
        req.release(req_id)

        mock_cloud.realtime.release.assert_called_once_with(req_id)

    @patch('picrawler.rt_cores.cloud')
    def test_with_with_statement(self, mock_cloud):
        with RTCoreRequest('c1', 10, 1):
            mock_cloud.realtime.request.assert_called_once_with('c1', 10, 1)
            eq_(0, mock_cloud.realtime.release.call_count)

        eq_(1, mock_cloud.realtime.release.call_count)


