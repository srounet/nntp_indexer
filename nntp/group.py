#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


class Group(object):

    def __init__(self, name):
        self.name = name

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

        self.count = None
        self.start = None
        self.end = None
        self.current = None

    def head(self, thread):
        _, count, first, last, name = thread.group(self.name)

        self.count = int(count)
        self.first = int(first)
        self.last = int(last)
        self.current = int(first)
        thread.working = False

    def xover(self, thread, start, end):
        start, end = str(start), str(end)

        thread.group(self.name)
        try:
            _, items = thread.xover(start, end)
            self.logger.info(
                'Group: {} - sent xover({} - {}) thread #{} of server: {}'.format(
                    self.name,
                    start,
                    end,
                    thread.thread_index,
                    thread.server_name
                )
            )
        except EOFError:
            return self.xover(thread, start, end)
        thread.working = False
        return items
