#!/usr/bin/env python
# -*- coding: utf-8

import urllib
import sqlite3

import nntp.exception
import nntp.plugins.base


class SqlitePlugin(nntp.plugins.base.BasePlugin):

    __type__ = 'sqlite'

    def __init__(self, config):
        if not 'filepath' in config:
            raise nntp.exception.InvalidConfigFile('filepath')

        self.filepath = config['filepath']
        self.setup()

    def setup(self):
        self.dbh = sqlite3.connect(self.filepath)
        self.dbh.execute("""
            CREATE TABLE IF NOT EXISTS headers(
              id text,
              subject text,
              author text,
              date text,
              message_id text,
              size text,
              lines text)
        """)

    def insert(self, record):
        id, subject, author, date, message_id, reference, size, lines = record
        subject = urllib.quote_plus(subject)
        self.dbh.execute("""
            INSERT INTO headers (id, subject, author, date, message_id, size, lines) values (?, ?, ?, ?, ?, ?, ?)
        """, (id, subject, author, date, message_id, size, lines))

    def select(self, record):
        pass
