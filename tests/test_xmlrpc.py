#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import xmlrpclib
from expects import *
from threading import Thread

from werkzeug_xmlrpc import WSGIXMLRPCApplication


class BasicTestMethods(unittest.TestCase):
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 3423
    DEFAULT_URI = 'http://' + DEFAULT_HOST + ':' + str(DEFAULT_PORT)

    @staticmethod
    def make_server(host=DEFAULT_HOST, port=DEFAULT_PORT):
        def test_1():
            return 'test_1_response'

        class Test2(object):
            def test_3(self, obj):
                return obj

        test = Test2()

        application = WSGIXMLRPCApplication(
            instance=test, methods=[test_1]
        )

        from wsgiref import simple_server

        server = simple_server.make_server(host, port, application)
        return server

    @staticmethod
    def make_client(uri=DEFAULT_URI):
        return xmlrpclib.ServerProxy(uri)

    def setUp(self):
        self.server = self.make_server()

        self.thread = Thread(target=self.server.serve_forever)

        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()


class TestXMLRPC(BasicTestMethods):
    def test_xmlrpc_server(self):
        client = self.make_client()

        expect(client.test_1()).to(equal('test_1_response'))
        expect(client.test_3({'trial dict': 4})).to(equal({'trial dict': 4}))
