#!/usr/bin/env python

"""
Install script for the snakefood dependency graph tool.
"""

__author__ = "Martin Blais <blais@furius.ca>"

import sys
from distutils.core import setup

def read_version():
    try:
        return open('VERSION', 'r').readline().strip()
    except IOError, e:
        raise SystemExit(
            "Error: you must run setup from the root directory (%s)" % str(e))

setup(name="antiorm",
      version=read_version(),
      description=\
      "Dependency Graphing for Python",
      long_description="""
Create a dependency graph from Python code.
""",
      license="GPL",
      author="Martin Blais",
      author_email="blais@furius.ca",
      url="http://furius.ca/snakefood",
      package_dir = {'': 'lib/python'},
      scripts = ['bin/snakefood']
     )


