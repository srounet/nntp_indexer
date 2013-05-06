#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import logging

import gevent
import gevent.monkey; gevent.monkey.patch_all()
import gevent.pool
import gevent.queue

import nntp.exception
import nntp.group
import nntp.plugin
import nntp.server


class Manager(object):
    def __init__(self, config):
        self.config = config

        self.groups = []
        self.plugins = {}
        self.pool_size = int(config['threads'])
        self.pool = gevent.pool.Pool(self.pool_size)
        self.queue = gevent.queue.Queue()
        self.roundrobin = config['roundrobin']
        self.servers = []

        self.logger = logging.getLogger('Manager')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

        self.load_plugins()
        self.setup_database()

    def terminate(self):
        self.running = False #XXX Use it

    def load_plugins(self):
        plugin_filenames = nntp.plugin.scan_folder('nntp/plugins')
        for plugin_name in plugin_filenames:
            plugin = nntp.plugin.load_module(plugin_name)
            plugin_type = plugin.__type__
            self.plugins[plugin_type] = plugin
            self.logger.info('Found database plugin: {}'.format(plugin_type))

    def connect(self):
        for account in self.config['accounts']:
            server = nntp.server.Server(**account)
            try:
                server.connect()
                self.servers.append(server)
            except nntp.exception.BadCredentials as e:
                self.logger.error(e)
        self.servers = itertools.cycle(self.servers)

    def disconnect(self):
        for server in self.servers:
            server.disconnect()

    def setup_database(self):
        database_type = self.config['database']['type']
        if not database_type in self.plugins:
            raise nntp.exception.NoSuchPlugin(database_type)
        self.logger.info('Manager - using database plugin: {}'.format(
            database_type))
        self.database = self.plugins[database_type](
            self.config['database']
        )

    @property
    def server(self):
        return next(self.servers)

    def add_group(self, groupname):
        group = nntp.group.Group(groupname)
        group.head(self.server.thread)
        if not self.database.has_group(groupname):
            self.database.add_group(groupname, group.first)
        group_status = self.database.group_status(groupname)
        group.current = group_status['current']
        self.groups.append(group)
        self.logger.info('Manager - added group: {}'.format(groupname))

    def on_item(self, g):
        records, groupname, end = g.value
        print records, groupname, end
        for record in records:
            if self.database.has_post(record['article_id']):
                self.logger.info("Manager - article exists: {}".format(
                    record['acticle_id']))
                continue
            self.database.insert(record)
        # Update group current
        self.database.update_group(
            groupname,
            end)

    def index(self):
        if not self.groups:
            return
        groups = itertools.cycle(self.groups)
        for group in groups:
            current = group.current
            group.current = group.current + 1000
            g = self.pool.spawn(
                group.xover,
                self.server.thread,
                current,
                current + 1000)
            g.link_value(self.on_item)

            if group.current > group.end:
                for index, gr in enumerate(self.groups):
                    if gr.name == group.name:
                        self.groups.pop(index)
                self.index()
