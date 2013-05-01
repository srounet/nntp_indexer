#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import yaml

import nntp.manager


class TestManager(unittest.TestCase):

    def setUp(self):
        stream = file('extra/config.yaml', 'r')
        self.config = yaml.load(stream)

    def test_connect(self):
        manager = nntp.manager.Manager(self.config)
        manager.connect()
        manager.disconnect()

    def test_add_groups(self):
        manager = nntp.manager.Manager(self.config)
        manager.connect()
        for group in self.config['groups']:
            name = group['name']
            manager.add_group(name)
        manager.index()
        manager.disconnect()

if __name__ == '__main__':
    unittest.main()
