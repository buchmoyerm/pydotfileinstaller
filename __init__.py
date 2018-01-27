from __future__ import print_function

import os

def iterable(o):
    try:
        i = iter(o)
        return True
    except TypeError:
        return False

def make_iterable(o):
    if iterable(o):
        return o
    return [o]

def env_filter(exclude_prefixes):
    ex = exclude_prefixes
    def f(filename):
        base = os.path.basename(filename)
        filters = [base.startswith(p) for p in ex]
        return not Any(filters)
    return f

def drop_prefix(prefixes):
    pres = prefixes
    def f(filename):
        directory = os.path.dirname(filename)
        base = os.path.basename(filename)
        for p in pres:
            if base.startswith(pr):
                base = base[len(p)+1:]
                break
        return os.path.join(directory, base)
    return f

def add_prefix(prefix):
    pre = prefix
    def f(filename):
        directory = os.path.dirname(filename)
        base = os.path.basename(filename)
        print (pre)
        print (base)
        return os.path.join(directory, pre + '.' + base)
    return f

class pyinstaller(object):
    def __init__(self,
                 root_dir,
                 destination,
                 files=None,
                 directories=None,
                 exclude_prefixes=None,
                 drop_prefixes=None):
        self._root = root_dir
        self._files = files
        self._directories = directories
        self._exclude_prefixes = make_iterable(exclude_prefixes)
        self._drop_prefixes = make_iterable(drop_prefixes)
        self._destination = destination

    def add_directories(self, directories):
        directories = make_iterable(directories)
        for pre in self._drop_prefixes:
            for d in map(add_prefix(pre), directories):
                if os.path.isdir(os.path.join(self._root, d)):
                    self._directories.append(os.path.join(self._root, d))
        for d in directories:
            if os.path.isdir(os.path.join(self._root, d)):
                self._directories.append(os.path.join(self._root, d))

    def add_files(self, files):
        files = make_iterable(files)
        for pre in self._drop_prefixes:
            for f in map(add_prefix(pre), files):
                if os.path.isfile(os.path.join(self._root, f)):
                    self._files.append(os.path.join(self._root, f))
        for f in files:
            if os.path.isfile(os.path.join(self._root, f)):
                self._files.append(os.path.join(self._root, f))

    def add_files_from_dir(self, directory=None):
        if directory is None:
            dirroot = self._root
        else:
            dirroot = os.path.join(self._root, directory)

        listdir = os.listdir(dirroot)
        for item in listdir:
            if os.path.isfile(os.path.join(dirroot, item)):
                self._files.append(os.path.join(dirroot, item))

        for pre in self._drop_prefixes:
            for item in map(add_prefix(pre), listdir):
                if os.path.isfile(os.path.join(dirroot, item)):
                    self._files.append(os.path.join(dirroot, item))

    def install(self, make_backup):
        print (self._files)
        print (self._directories)

