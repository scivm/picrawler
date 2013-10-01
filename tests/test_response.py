# -*- coding: utf-8 -*-

from nose.tools import *
from mock import Mock
import pickle

from picrawler.response import BaseResponse, Response, ErrorResponse


class TestBaseResponse(object):
    def test_constructor(self):
        request_mock = Mock()
        ins = BaseResponse(request_mock)
        eq_(ins.request, request_mock)

    def test_run_callback(self):
        request_mock = Mock()
        ins = BaseResponse(request_mock)
        ins.run_callback()
        request_mock.run_callback.called_once_with(ins)

    def test_pickle_instance(self):
        request_mock = {}
        ins = BaseResponse(request_mock)
        ins2 = pickle.loads(pickle.dumps(ins))
        eq_(ins.__dict__, ins2.__dict__)


class TestResponse(object):
    def test_constructor(self):
        request_mock = Mock()
        ins = Response(request_mock, 200, 'dummy', dict(name='value'))

        eq_(200, ins.status_code)
        eq_('dummy', ins.content)
        eq_(dict(name='value'), ins.headers)
        eq_(ins.request, request_mock)


class TestErrorResponse(object):
    def test_constructor(self):
        request_mock = Mock()
        exception = Exception('error')
        ins = ErrorResponse(request_mock, exception)

        eq_(exception, ins.exception)
        eq_(ins.request, request_mock)
