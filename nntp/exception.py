#!/usr/bin/rnv python
# -*- coding: utf-8 -*-

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
