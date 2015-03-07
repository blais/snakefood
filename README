=========================================
   snakefood: Python Dependency Graphs
=========================================

.. contents::
..
    1  Description
      1.1  Tools Included
    2  Dependencies
    3  Documentation
    4  Download
    5  Copyright and License
    6  Author

Description
===========

Generate dependency graphs from Python code.  This dependency tracker
package has a few distinguishing characteristics:

- It uses the AST to parse the Python files. This is **very
  reliable**, it always runs.

- **No module is loaded**. Loading modules to figure out dependencies
  is almost always problem, because a lot of codebases run
  initialization code in the global namespace, which often requires
  additional setup. Snakefood is guaranteed not to have this problem
  (it just runs, no matter what).

- It works on a set of files, i.e. you do not have to specify a single
  script, you can select a directory (package or else) or a set of
  files.  It finds all the Python files recursively automatically.

- **Automatic/no configuration**: your PYTHONPATH is automatically
  adjusted to include the required package roots. It figures out the
  paths that are required from the files/directories given as input.
  You should not have to setup ANYTHING.

- It does not have to automatically 'follow' dependencies between
  modules, i.e. by default it only considers the files and directories
  you specify on the command-line and their immediate dependencies.
  It also has an option to automatically include only the dependencies
  within the packages of the files you specify.

- It follows the UNIX philosophy of **small programs that do one thing
  well**: it consists of a few simple programs whose outputs you
  combine via pipes. Graphing dependencies always requires the user to
  filter and cluster the filenames, so this is appropriate. You can
  combine it with your favourite tools, grep, sed, etc.

A problem with dependency trackers that run code is that they are
unreliable, due to the dynamic nature of Python (the presence of
imports within function calls and __import__ hooks makes it almost
impossible to always do the right thing). This script aims at being
right 99% of the time, and we think that given the trade-offs, 99% is
good enough for 99% of the uses.

I fully intend that this program work on all codebases.  It has been
tested on a number of popular open source codes (see the test
directory).

Tools Included
--------------

#. ``sfood``:

     Given a set of input files or root directories, generate a list
     of dependencies between the files;

#. ``sfood-graph``:

     Read a list of dependencies and produce a Graphviz dot file.
     (This file can be run through the Graphviz ``dot`` tool to
     produce a viewable/printable PDF file);

#. ``sfood-cluster``:

     Read a list of dependencies, a list of file clusters, and output
     a list of simplified (clustered) dependencies.

#. ``sfood-checker``:

     Analyze the source code with the AST and list unused or
     redundant imports.

#. ``sfood-imports``:

     Find and list import statements in Python files, regardless of
     whether they can be imported or not.

See `full documentation </snakefood/doc/snakefood-doc.html>`_ for more
details.


Dependencies
============

- Python 2.7 or higher.  Python-3.x works too.
- The Python "six" library.


Documentation
=============

- `CHANGES <CHANGES>`_
- `TODO <TODO>`_

- `User's Manual </snakefood/doc/snakefood-doc.html>`_
- `Example Outputs </snakefood/doc/examples/>`_


Download
========

A Mercurial repository can be found at:

  http://bitbucket.org/blais/snakefood


Links
=====

- `dottoxml
  <http://www.mydarc.de/dl9obn/programming/python/dottoxml/>`_, a tool
  by Dirk Bächle, that converts dot files into yEd inputs, useful for
  large graphs.

Copyright and License
=====================

Copyright (C) 2001-2007  Martin Blais.  All Rights Reserved.

This code is distributed under the `GNU General Public License <COPYING>`_;


Author
======

Martin Blais <blais@furius.ca>
