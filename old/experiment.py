## try:
##     from imp import get_loader
## except ImportError:
##     from pkgutil import get_loader

from imp import find_module
from pkgutil import ImpImporter
from os.path import *

def find_mod(modname, fn):

    print '\n\n\n-----', modname, fn

    mod = ImpImporter().find_module(modname)
    print 'global', mod, mod and mod.get_filename()

    mod = ImpImporter(dirname(fn)).find_module(modname)
    print 'local', mod, mod and mod.get_filename()

    try:
        mod = find_module(modname)
    except ImportError:
        mod = 'ERROR'
    print 'imp global', mod

    try:
        mod = find_module(modname, dirname(fn))
    except ImportError:
        mod = 'ERROR'
    print 'imp local', mod





## print find_module('ctypes.util')
## print find_module('util', '/usr/lib/python2.5/ctypes/__init__.py')
## raise SystemExit



import sys, os, os.path
find_mod('sys', os.__file__)
find_mod('os', os.__file__)
find_mod('os.path', os.path.__file__)

## import mt
## find_mod('mt', mt.__file__)
## find_mod('mt.core', mt.__file__)

from mt.util import func
find_mod('maths', func.__file__)
find_mod('mt.util.maths', func.__file__)
find_mod('mt.util.pxfloat', func.__file__)

import ctypes, logging
find_mod('ctypes.util', ctypes.__file__)
find_mod('logging.config', logging.__file__)
