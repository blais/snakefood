#!/usr/bin/env python
"""
Install script for the snakefood dependency graph tool.
"""

__author__ = "Martin Blais <blais@furius.ca>"

import os
from os.path import join, isfile
from distutils.core import setup
import sys


# Install all scripts under bin.
scripts = list(filter(isfile, [join('bin', x) for x in os.listdir('bin')]))

def read_version():
    try:
        return open('VERSION', 'r').readline().strip()
    except IOError:
        _, e, _ = sys.exc_info()
        raise SystemExit(
            "Error: you must run setup from the root directory (%s)" % str(e))


# Include all files without having to create MANIFEST.in
def add_all_files(fun):
    import os, os.path
    from os.path import abspath, dirname, join
    def f(self):
        for root, dirs, files in os.walk('.'):
            if '.hg' in dirs: dirs.remove('.hg')
            self.filelist.extend(join(root[2:], fn) for fn in files
                                 if not fn.endswith('.pyc'))
        return fun(self)
    return f
from distutils.command.sdist import sdist
sdist.add_defaults = add_all_files(sdist.add_defaults)


setup(name="snakefood",
      version=read_version(),
      description=\
      "Dependency Graphing for Python",
      long_description="""
Generate dependencies from Python code, filter, cluster and generate graphs
from the dependency list.
""",
      license="GPL",
      author="Martin Blais",
      author_email="blais@furius.ca",
      url="http://furius.ca/snakefood",
      download_url="http://bitbucket.org/blais/snakefood",
      package_dir = {'': 'lib/python'},
      packages = ['snakefood', 'snakefood/fallback'],
      scripts=scripts
     )
