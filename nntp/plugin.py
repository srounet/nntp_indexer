#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nntp.plugins.base
import inspect
import os


def scan_folder(dirpath):
    dirpath = os.path.abspath(dirpath)
    if not os.path.exists(dirpath):
        raise IOError("No such folder exists: {}".format(dirpath))
    if not os.path.isdir(dirpath):
        raise IOError("Given dirpath is not a directory: {}".format(dirpath))

    filenames = os.listdir(dirpath)
    filenames = [
        os.path.splitext(filename)[0] for filename in filenames
        if not os.path.splitext(filename)[1] == '.pyc'
    ]
    wildcards = ['__init__', 'base']
    plugin_filenames = [
        name for name in filenames
        if not name in wildcards
    ]
    return plugin_filenames


def load_module(module_name):
    import_path = 'nntp.plugins.{}'.format(module_name)

    module_import_path, objname = import_path.rsplit('.', 1)
    module = __import__(module_import_path, fromlist=[objname])
    module = getattr(module, objname)
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            if obj.__bases__[0] == nntp.plugins.base.BasePlugin:
                if not hasattr(obj, '__type__'):
                    raise nntp.exception.InvalidPlugin(name)
                return obj



if __name__ == '__main__':
    plugin_filenames = scan_folder("nntp/plugins")
    for n in plugin_filenames:
        obj = load_module(n)
        print obj
