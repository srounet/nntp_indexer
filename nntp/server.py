#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import logging
import nntplib

import gevent.monkey; gevent.monkey.patch_all()

import nntp.exception


class Server(object):

    def __init__(self, username, password, host, port, threads):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.thread_count = threads

        self.connected = False
        self.threads = []

        self.logger = logging.getLogger(self.host)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    def connect(self):
        for thread_index in range(self.thread_count):
            try:
                server = nntplib.NNTP(
                    self.host,
                    self.port,
                    self.username,
                    self.password)
                self.logger.info('Server: {} - Thread #{} connected'.format(
                        self.host,
                        thread_index))
                server.server_name = self.host
                server.thread_index = thread_index
                server.working = False
                self.threads.append(server)
            except Exception:
                continue

        if not self.threads:
            raise nntp.exception.BadCredentials(
                server = self.host,
                username = self.username,
                password = self.password)
        self.threads = itertools.cycle(self.threads)

    def disconnect(self):
        for thread_index, thread in enumerate(self.threads):
            thread.quit()
            self.logger.info('{} - Thread #{} disconnected'.format(
               self.host,
               thread_index
            ))

    @property
    def thread(self):
        while True:
            thread = next(self.threads)
            if not thread.working:
                thread.working = True
                return thread
