#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml

import nntp.manager


if __name__ == '__main__':
    stream = file('extra/config.yaml', 'r')
    config = yaml.load(stream)
    manager = nntp.manager.Manager(config)
    manager.connect()
    for group in config['groups']:
        name = group['name']
        manager.add_group(name)
    manager.index()

