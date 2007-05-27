"""
Code that deals with search and classifying root directories.
"""

import os, logging
from os.path import *
from dircache import listdir

from util import is_python

__all__ = ('find_roots', 'find_package_root', 'search_for_roots',
           'is_package_dir', 'is_package_root', 'relfile',)


def find_roots(list_dirofn, _):
    """
    Given a list of directories or filenames, find Python files and calculate
    the entire list of roots.
    """
    inroots = set()
    for fn in map(realpath, list_dirofn):

        # Search up the directory tree for a root.
        root = find_package_root(fn)
        if root:
            inroots.add(root)
        else:
            # If the given file is not sitting within a root, search down the
            # directory tree for available roots.
            downroots = search_for_roots(fn)
            if downroots:
                inroots.update(downroots)
            else:
                assert isdir(fn)
                logging.warning("Directory '%s' does live or include any roots." % fn)
    return sorted(inroots)

def find_package_root(dn):
    "Search up the directory tree for a package root."
    if not isdir(dn):
        dn = dirname(dn)
    while is_package_dir(dn):
        dn = dirname(dn)
    if is_package_root(dn):
        return dn

def search_for_roots(dn):
    """Search down the directory tree for package roots.  The recursive search
    does not move inside the package root when one is found."""
    if not isdir(dn):
        dn = dirname(dn)
    roots = []
    for root, dirs, files in os.walk(dn):
        if is_package_root(root):
            roots.append(root)
            dirs[:] = []
    return roots

def is_package_dir(dn):
    """Return true if this is a directory within a package."""
    return exists(join(dn, '__init__.py'))


filesets_ignore = (['setup.py'],)
maxlen_filesets = max(map(len, filesets_ignore))

def is_package_root(dn):
    """Return true if this is a package root.  A package root is a directory
    that could be used as a PYTHONPATH entry."""

    if exists(join(dn, '__init__.py')):
        return False
    else:
        # Check if the directory contains Python files.
        files = listdir(dn)
        pyfiles = []
        for x in [join(dn, x) for x in files]:
            ## FIXME: should we use opts.ignore here too?
            if x.endswith('.so') or is_python(x):
                pyfiles.append(x)
                if len(pyfiles) > maxlen_filesets:
                    break

        # Note: we skip directories which only contain a single distutils
        # setup.py file.
        if pyfiles and pyfiles not in filesets_ignore:
            return True

        # Note: We make use of the fact that dotted directory names cannot be
        # imported as packaged.
        for sub in files:
            if '.' in sub:
                continue
            sub = join(dn, sub)
            if not isdir(sub):
                continue
            if exists(join(sub, '__init__.py')):
                return True

    return False

def relfile(fn):
    "Return pairs of (package root, relative filename)."
    root = find_package_root(realpath(fn))
    assert root is not None, fn
    return root, fn[len(root)+1:]


