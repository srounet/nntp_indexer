#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import urllib

import nntp.exception
import nntp.plugins.base


class MongoPlugin(nntp.plugins.base.BasePlugin):

    __type__ = 'mongo'

    def __init__(self, config):
        if not 'database' in config:
            raise nntp.exception.InvalidConfigFile('database')
        if not 'collection' in config:
            raise nntp.exception.InvalidConfigFile('collection')
        #XXX Handle login/pw host/port

        self.database = config['database']
        self.collection = config['collection']
        self.setup()

    def setup(self):
        database = pymongo.Connection()
        self.dbh = database[self.database][self.collection]

    def insert(self, record):
        id, subject, author, date, message_id, reference, size, lines = record
        subject = urllib.quote_plus(subject)
        self.dbh.insert({
            'id': id,
            'subject': subject,
            'author': author,
            'date': date,
            'message_id': message_id,
            'size': size,
            'lines': lines
        })
