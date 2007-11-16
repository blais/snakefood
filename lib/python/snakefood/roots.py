"""
Code that deals with search and classifying root directories.
"""
# This file is part of the Snakefood open source package.
# See http://furius.ca/snakefood/ for licensing details.

import os, logging
from os.path import *
from dircache import listdir

from snakefood.util import is_python, filter_separate

__all__ = ('find_roots', 'find_package_root', 'relfile',)



def find_roots(list_dirofn, ignores):
    """
    Given a list of directories or filenames, find Python files and calculate
    the entire list of roots.
    """
    inroots = set()
    for fn in map(realpath, list_dirofn):

        # Search up the directory tree for a root.
        root = find_package_root(fn, ignores)
        if root:
            inroots.add(root)
        else:
            # If the given file is not sitting within a root, search down the
            # directory tree for available roots.
            downroots = search_for_roots(fn, ignores)
            if downroots:
                inroots.update(downroots)
            else:
                assert isdir(fn)
                logging.warning("Directory '%s' does live or include any roots." % fn)
    return sorted(inroots)

def find_package_root(dn, ignores):
    "Search up the directory tree for a package root."
    if not isdir(dn):
        dn = dirname(dn)
    while is_package_dir(dn):
        assert dn
        dn = dirname(dn)
    if dn and is_package_root(dn, ignores):
        return dn

def search_for_roots(dn, ignores):
    """Search down the directory tree for package roots.  The recursive search
    does not move inside the package root when one is found."""
    if not isdir(dn):
        dn = dirname(dn)
    roots = []
    for root, dirs, files in os.walk(dn):
        for d in list(dirs):
            if d in ignores:
                dirs.remove(d)
        if is_package_root(root, ignores):
            roots.append(root)
            dirs[:] = []
    return roots

def is_package_dir(dn):
    """Return true if this is a directory within a package."""
    return exists(join(dn, '__init__.py'))


filesets_ignore = (['setup.py'],)
maxlen_filesets = max(map(len, filesets_ignore))

def is_package_root(dn, ignores):
    """Return true if this is a package root.  A package root is a directory
    that could be used as a PYTHONPATH entry."""

    if exists(join(dn, '__init__.py')):
        return False

    else:
        dirfiles = (join(dn, x) for x in listdir(dn))
        subdirs, files = filter_separate(isdir, dirfiles)

        # Check if the directory contains Python files.
        pyfiles = []
        for x in files:
            bx = basename(x)
            if bx in ignores:
                continue
            if bx.endswith('.so') or is_python(x):
                pyfiles.append(bx)
                if len(pyfiles) > maxlen_filesets:
                    break

        # Note: we skip directories which only contain a single distutils
        # setup.py file.
        if pyfiles and pyfiles not in filesets_ignore:
            return True

        # Check if the directory contains Python packages.
        for sub in subdirs:
            bsub = basename(sub)
            # Note: Make use of the fact that dotted directory names cannot be
            # imported as packages for culling away branches by removing those
            # subdirectories that have dots in them.
            if '.' in bsub or bsub in ignores:
                continue
            if exists(join(sub, '__init__.py')):
                return True

    return False

def relfile(fn, ignores):
    "Return pairs of (package root, relative filename)."
    root = find_package_root(realpath(fn), ignores)
    if root is None:
        assert basename(fn) in filesets_ignore[0], fn
        return
    return root, fn[len(root)+1:]


