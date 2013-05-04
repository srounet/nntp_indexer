#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BasePlugin(object):
    def insert(self, record):
        raise NotImplementedError

    def select(self, record):
        raise NotImplementedError
