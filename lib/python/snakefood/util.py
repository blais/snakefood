"""
Various utilities, to iterate among files, for example.
"""

import os, logging, re
from os.path import *


_iter_ignores = ['.svn', 'CVS', 'build']
# Note: 'build' is for those packages which have been installed with setup.py.
# It is pretty common to forget these around.

def iter_pyfiles(dirsorfns, ignores=None, abspaths=False):
    """Yield all the files ending with .py recursively.  'dirsorfns' is a list
    of filenames or directories.  If 'abspaths' is true, we assumethe paths are
    absolute paths."""
    assert isinstance(dirsorfns, (list, tuple))
    assert isinstance(ignores, list)

    ignores = ignores or _iter_ignores
    for dn in dirsorfns:
        if not abspaths:
            dn = realpath(dn)

        if not exists(dn):
            logging.warning("File '%s' does not exist." % dn)
            continue

        if not isdir(dn):
            if is_python(dn):
                yield dn

        else:
            for root, dirs, files in os.walk(dn):
                for r in ignores:
                    try:
                        dirs.remove(r)
                    except ValueError:
                        pass

                afiles = [join(root, x) for x in files]
                for fn in filter(is_python, afiles):
                    yield fn

def is_python(fn):
    "Return true if the file is a Python file."
    if fn.endswith('.py'):
        return True
    else:
        try:
            file_head = open(fn).read(64)
            if re.match("#!.*\\bpython", file_head):
                return True
        except IOError:
            return False

