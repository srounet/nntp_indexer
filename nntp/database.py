#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import sqlite3


class Database(object):
    def insert(self, record):
        raise NotImplementedError

    def select(self, record):
        raise NotImplementedError


class SqliteDatabase(Database):

    def __init__(self, filepath):
        self.filepath = filepath
        self.dbh = sqlite3.connect(self.filepath)

        self.setup()

    def setup(self):
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
