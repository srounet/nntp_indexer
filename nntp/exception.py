#!/usr/bin/rnv python
# -*- coding: utf-8 -*-

class InvalidPlugin(Exception):
    def __init__(self, name):
        self.name

    def __str__(self):
        message = "Invalid plugin: {}".format(self.name)
        return message


class NoSuchPlugin(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        message = "No such plugin exists: {}".format(self.name)
        return message


class InvalidConfigFile(Exception):
    def __init__(self, missing_key):
        self.missing_key = missing_key

    def __str__(self):
        message = "Missing key in config file: {}".format(self.missing_key)
        return message


class NntpIndexerException(Exception):
    def __int__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class BadCredentials(NntpIndexerException):
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password

    def __str__(self):
        message = 'Server: {} - Bad credentials (username:{}, password:{}'.format(
            self.server,
            self.username,
            self.password
        )
        return message

class BadGroup(NntpIndexerException):
    def __init__(self, groupname):
        self.groupname = groupname

    def __str__(self):
        message = 'Bad group name: {}'.format(self.groupname)
        return message
