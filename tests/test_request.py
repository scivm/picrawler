# -*- coding: utf-8 -*-

from nose.tools import *
from mock import Mock, patch
import re

from picrawler import request
from picrawler.request import Request
from picrawler.response import Response, ErrorResponse


class TestRequest(object):
    def test_constructor(self):
        Request('http://dummy', 'get')

    @raises(request.InvalidHTTPMethod)
    def test_constructor_with_invalid_method(self):
        Request('http://dummy', 'dummy')

    def test_id(self):
        req = Request('http://dummy', 'get')
        ok_(re.match(r'^[0-9a-f]{32}$', req.id))

    def test_run_success_callback(self):
        mock_success_cb = Mock()

        req = Request('http://dummy', success_callback=mock_success_cb)

        mock_resp = Response(req, 200, 'content', {})
        req.run_callback(mock_resp)

        mock_success_cb.assert_called_once_with(mock_resp)

    def test_run_error_callback(self):
        mock_error_cb = Mock()

        req = Request('http://dummy', error_callback=mock_error_cb)

        mock_resp = ErrorResponse(req, Exception())
        req.run_callback(mock_resp)

        mock_error_cb.assert_called_once_with(mock_resp)

    @raises(request.InvalidResponse)
    def test_run_callback_with_invalid_response(self):
        req = Request('http://dummy')
        req.run_callback({})

    @patch('requests.get')
    def test_call(self, requests_get):
        req = request.Request('http://dummy', 'GET')
        ret = req()

        ok_(isinstance(ret, Response))

        (args, kwargs) = requests_get.call_args
        eq_('http://dummy', args[0])

    @patch('requests.get')
    def test_call_with_error(self, requests_get):
        req = request.Request('http://dummy', 'GET')
        exception = Exception('error')
        requests_get.side_effect = exception

        ret = req()

        ok_(isinstance(ret, ErrorResponse))
        eq_(exception, ret.exception)
