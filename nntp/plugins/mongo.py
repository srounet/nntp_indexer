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
        #XXX Handle login/pw host/port

        self.database = config['database']
        self.setup()

    def setup(self):
        database = pymongo.Connection()
        self.dbh = database[self.database]

    def has_group(self, groupname):
        group = self.dbh['groups'].find_one({'name': groupname})
        group_exists = bool(group)
        return group_exists

    def add_group(self, groupname, first):
        self.dbh['groups'].insert({
            'name': groupname,
            'first': first,
            'current': first
        })

    def update_group(self, groupname, current):
        self.dbh['groups'].update(
            {'name': groupname},
            {'$set': {'current': current}}
        )

    def group_status(self, groupname):
        group = self.dbh['groups'].find_one({'name': groupname})
        return group

    def has_post(self, article_id):
        post = self.dbh['posts'].find_one({'id': article_id})
        post_exists = bool(post)
        return post_exists

    def insert(self, record):
        record['subject'] = urllib.quote_plus(record['subject'])

        record.pop('reference')
        self.dbh['posts'].insert(record)
