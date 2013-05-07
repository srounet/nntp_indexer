#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import gevent
import urllib

import nntp.exception
import nntp.plugins.base


class MongoPlugin(nntp.plugins.base.BasePlugin):

    __type__ = 'mongo'

    def __init__(self, config):
        """A mongo database plugin.

        Note: actually the system plugin does not allow to have multiple
        database instance for each server thread, that's why we have to trick
        the AutoReconnect exception. With too much thread we will reach mongodb
        max connection in minutes.
        """
        if not 'database' in config:
            raise nntp.exception.InvalidConfigFile('database')
        #XXX Handle login/pw host/port

        self.database = config['database']
        self.host = config.get('host')
        self.port = config.get('port') or 27017
        self.setup()

    def setup(self):
        database = pymongo.Connection(
            self.host,
            self.port,
            max_pool_size=10,
            use_greenlets=True
        )
        self.db = database
        self.dbh = self.db[self.database]
        self.posts = self.dbh['posts']
        self.groups = self.dbh['groups']

    def has_group(self, groupname):
        while True: #Trick around mongodb max connections
            try:
                group = self.groups.find_one({'name': groupname})
                break
            except pymongo.errors.AutoReconnect:
                gevent.sleep(5)
        group_exists = bool(group)
        return group_exists

    def add_group(self, groupname, first):
        while True: #Trick around mongodb max connections
            try:
                self.groups.insert({
                    'name': groupname,
                    'first': first,
                    'current': first
                })
                break
            except pymongo.errors.AutoReconnect:
                gevent.sleep(5)

    def update_group(self, groupname, current):
        while True: #Trick around mongodb max connections
            try:
                self.groups.update(
                    {'name': groupname},
                    {'$set': {'current': current}}
                )
                break
            except pymongo.errors.AutoReconnect:
                gevent.sleep(5)

    def group_status(self, groupname):
        while True: #Trick around mongodb max connections
            try:
                group = self.groups.find_one({'name': groupname})
                break
            except pymongo.errors.AutoReconnect:
                gevent.sleep(5)
        return group

    def has_post(self, article_id):
        while True: #Trick around mongodb max connections
            try:
                post = self.posts.find_one({'id': article_id})
                break
            except pymongo.errors.AutoReconnect:
                gevent.sleep(5)
        post_exists = bool(post)
        return post_exists

    def insert(self, record):
        record['subject'] = urllib.quote_plus(record['subject'])

        record.pop('reference')
        while True: #Trick around mongodb max connections
            try:
                self.posts.insert(record)
                break
            except pymongo.errors.AutoReconnect:
                gevent.sleep(5)
