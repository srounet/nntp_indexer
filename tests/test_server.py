#!usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import nntp.exception
import nntp.server
import yaml


class TestServer(unittest.TestCase):

    def setUp(self):
        stream = file('extra/config.yaml', 'r')
        self.config = yaml.load(stream)

    def test_connect(self):
        for account in self.config['accounts']:
            server = nntp.server.Server(**account)
            server.connect()
            server.disconnect()

    def bad_credentials(self):
        credentials = {
            'host': 'eu.news.astraweb.com',
            'port': 119,
            'username': 'bad_username',
            'password': 'bad_password',
        }
        server = nntp.server.Server(**credentials)
        self.assertRaises(
            nntp.exception.BadCredentials,
            server.connect
        )


if __name__ == '__main__':
    unittest.main()
