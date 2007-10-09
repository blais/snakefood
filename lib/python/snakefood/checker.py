#!/usr/bin/env python
"""Check for superfluous import statements in Python source code.

This script is used to detect forgotten imports that are not used anymore. When
writing Python code (which happens so fast), it is often the case that we forget
to remove useless imports.

This is implemented using a search in the AST, and as such we do not require to
import the module in order to run the checks. This is a major advantage over all
the other lint/checker programs, and the main reason for taking the time to
write it.
"""

__author__ = "Martin Blais <blais@furius.ca>"
__copyright__ = """Copyright (C) 2007 Martin Blais <blais@furius.ca>.
This code is distributed under the terms of the GNU General Public License."""

# stdlib imports
import sys
from os.path import *
import compiler

from snakefood.util import def_ignores, iter_pyfiles
from snakefood.astpretty import printAst


def main():
    import optparse
    parser = optparse.OptionParser(__doc__.strip())

    parser.add_option('-v', '--verbose', action='store_true',
                      help="Verbose (debugging) output.")

    parser.add_option('-I', '--ignore', dest='ignores', action='append',
                      default=def_ignores,
                      help="Add the given directory name to the list to be ignored.")

    opts, args = parser.parse_args()

    write = sys.stderr.write
    for fn in iter_pyfiles(args or ['.'], opts.ignores, False):

        # Convert the file to an AST.
        try:
            mod = compiler.parseFile(fn)
        except SyntaxError, e:
            write("%s:%s: %s.\n" % (fn, e.lineno, e))
            continue

        # Find all the imports.
        vis = ImportVisitor()
        compiler.walk(mod, vis)
        imported = vis.finalize()

        # Check for redundant imports.
        uimported = []
        simp = set()
        for x in imported:
            modname, lineno = x
            if modname in simp:
                write("%s:%d: Redundant import '%s'\n" % (fn, lineno, modname))
            else:
                uimported.append(x)
                simp.add(modname)
        imported = uimported

        vis = NamesVisitor()
        compiler.walk(mod, vis)
        names = vis.finalize()

        names = frozenset(names) # uniquify
        for modname, lineno in imported:
            if modname not in names:
                write("%s:%d: Unused symbol '%s'\n" % (fn, lineno, modname))

        if opts.verbose:
            print 'Imported names:'
            for modname, lineno in sorted(imported):
                print '  [%d] %s' % (lineno, modname)
            print

            print 'Used names:'
            for name in sorted(names):
                print '  %s' % name
            print

            print 'AST:'
            print '  ', printAst(mod)



class ImportVisitor(object):
    """AST visitor that accumulates the target names of import statements."""
    def __init__(self):
        self.symbols = []

    def visitImport(self, node):
        self.symbols.extend((x[1] or x[0], node.lineno) for x in node.names)

    def visitFrom(self, node):
        modname = node.modname
        if modname == '__future__':
            return # Ignore these.
        for name, as_ in node.names:
            if name != '*':
                self.symbols.append((as_ or name, node.lineno))

    def finalize(self):
        return self.symbols


class NamesVisitor(object):
    """AST visitor that finds all the identifier references that are not within
    import statements. This includes all free names and names with attribute
    references."""
    def __init__(self):
        self.names = []
        self.attributes = []

    def visitName(self, node):
        self.attributes.append(node.name)
        self.attributes.reverse()
        attribs = self.attributes
        for i in xrange(1, len(attribs)+1):
            self.names.append('.'.join(attribs[0:i]))
        self.attributes = []

    def visitGetattr(self, node):
        self.attributes.append(node.attrname)
        for child in node.getChildNodes():
            self.visit(child)

    def finalize(self):
        return self.names


class AssignVisitor(object):
    """AST visitor that builds a list of names being assigned to. This is used
    later to figure out if a name being refered to is never assigned to nor in
    the imports."""

    ## FIXME: TODO




if __name__ == '__main__':
    main()
    # For tests, see snakefood/test/snakefood.


