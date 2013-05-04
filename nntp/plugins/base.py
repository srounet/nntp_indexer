#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BasePlugin(object):
    def insert(self, record):
        raise NotImplementedError

    def select(self, record):
        raise NotImplementedError

    def had_group(self, groupname):
        raise NotImplementedError

    def add_group(self, groupname, first):
        raise NotImplementedError

    def update_group(self, groupname, current):
        raise NotImplementedError

    def group_status(self, groupname):
        raise NotImplementedError

    def has_post(self, article_id):
        raise NotImplementedError
