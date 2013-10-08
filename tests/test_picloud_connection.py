# -*- coding: utf-8 -*-

from nose.tools import *
from mock import Mock, patch

from picrawler.picloud_connection import PiCloudConnection
from picrawler import picloud_connection
from picrawler import request


class TestPiCloudConnection(object):
    @patch('picrawler.picloud_connection.cloud')
    def test_context_manager(self, mock_cloud):
        conn = PiCloudConnection()
        with conn:
            ok_(conn.is_connected)

        ok_(not conn.is_connected)

    @patch('picrawler.picloud_connection.cloud')
    def test_connect(self, mock_cloud):
        conn = PiCloudConnection()
        conn.connect()
        ok_(conn.is_connected)
        conn.close()

    @patch('picrawler.picloud_connection.cloud')
    def test_connect_initialize_queues(self, mock_cloud):
        conn = PiCloudConnection(max_parallel_jobs=100, core_type='c1')
        conn.connect()

        eq_(2, mock_cloud.queue.get.call_count)
        call_args = mock_cloud.queue.get.call_args_list

        request_queue_args = call_args[0][0]
        ok_(request_queue_args[0].startswith(picloud_connection.REQUEST_QUEUE_PREFIX))

        result_queue_args = call_args[1][0]
        ok_(result_queue_args[0].startswith(picloud_connection.RESULT_QUEUE_PREFIX))

        eq_(1, conn.request_queue.attach.call_count)
        (args, kwargs) = conn.request_queue.attach.call_args

        eq_([conn.result_queue], kwargs['output_queues'])
        eq_(100, kwargs['max_parallel_jobs'])
        eq_('c1', kwargs['_type'])

    @patch('picrawler.picloud_connection.cloud')
    def test_close(self, mock_cloud):
        conn = PiCloudConnection()
        conn.connect()

        conn.close()

        mock_cloud.close.assert_called_once_with()
        ok_(not conn.is_connected)

    @patch('picrawler.picloud_connection.cloud')
    def test_close_destroy_queues(self, mock_cloud):
        conn = PiCloudConnection()
        conn.connect()

        request_queue = conn.request_queue
        result_queue = conn.result_queue

        conn.close()

        request_queue.delete.assert_called_with()
        eq_(None, conn.request_queue)
        result_queue.delete.assert_called_with()
        eq_(None, conn.result_queue)

    @patch('picrawler.picloud_connection.cloud')
    def test_send(self, mock_cloud):
        conn = PiCloudConnection()
        conn.connect()

        requests = [request.Request('http://dummy') for n in range(3)]
        results = [Mock() for n in range(3)]
        results[0].request.id = requests[1].id
        results[1].request.id = requests[2].id
        results[2].request.id = requests[0].id

        conn._loop = Mock()
        conn._loop.return_value = results

        ret = conn.send(requests)

        conn._request_queue.push.assert_called_once_with(requests)
        conn._loop.assert_called_once_with()
        # results should be sorted in the order of requests
        eq_([results[2], results[0], results[1]], ret)


    @patch('picrawler.picloud_connection.cloud')
    @raises(picloud_connection.InvalidRequest)
    def test_send_with_none(self, mock_cloud):
        conn = PiCloudConnection()
        conn.connect()

        conn.send(None)

    @patch('picrawler.picloud_connection.cloud')
    @raises(picloud_connection.InvalidRequest)
    def test_send_with_invalid_list(self, mock_cloud):
        conn = PiCloudConnection()
        conn.connect()
        req = request.Request('http://dummy')

        conn.send([req, None])

    @patch('picrawler.picloud_connection.cloud')
    def test_loop(self, mock_cloud):
        conn = PiCloudConnection()
        conn.connect()

        mock_request_completed = Mock()
        mock_request_completed.side_effect = [False, True]
        conn._requests_completed = mock_request_completed

        mock_result_queue = Mock()
        result1 = Mock()
        result2 = Mock()
        mock_result_queue.pop.side_effect = [[result1], [result2]] + [None] * 2
        conn._result_queue = mock_result_queue

        ret = conn._loop()

        eq_([result1, result2], ret)
        result1.run_callback.assert_called_once_with()
        result2.run_callback.assert_called_once_with()

    @patch('picrawler.picloud_connection.cloud')
    def test_requests_completed(self, mock_cloud):
        conn = PiCloudConnection()
        conn.connect()

        mock_request_queue = Mock()
        conn._request_queue = mock_request_queue

        mock_result_queue = Mock()
        conn._result_queue = mock_result_queue

        def set_queue_info(request_count=0,
                           request_processing_jobs=0,
                           request_queued_jobs=0,
                           result_count=0):
            mock_request_queue.info.return_value = dict(
                count=request_count,
                processing_jobs=request_processing_jobs,
                queued_jobs=request_queued_jobs
            )
            mock_result_queue.count.return_value = result_count

        set_queue_info()
        ok_(conn._requests_completed())

        set_queue_info(request_count=1)
        ok_(not conn._requests_completed())

        set_queue_info(request_processing_jobs=1)
        ok_(not conn._requests_completed())

        set_queue_info(request_queued_jobs=1)
        ok_(not conn._requests_completed())

        set_queue_info(result_count=1)
        ok_(not conn._requests_completed())
