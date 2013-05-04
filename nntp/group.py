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
        _, count, first, end, name = thread.group(self.name)

        self.count = int(count)
        self.first = int(first)
        self.end = int(end)
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
        records = [{
            'group': self.name,
            'article_id': int(record[0]),
            'subject': record[1],
            'author': record[2],
            'date': record[3],
            'message_id': record[4],
            'reference': record[5],
            'size': int(record[6]),
            'lines': int(record[7])
        } for record in items]
        return records, self.name, int(end)
