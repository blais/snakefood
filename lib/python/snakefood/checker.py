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
import sys, __builtin__, re
from os.path import *
import compiler

from snakefood.util import def_ignores, iter_pyfiles
from snakefood.find import parse_python_source, check_duplicate_imports
from snakefood.astpretty import printAst


def main():
    import optparse
    parser = optparse.OptionParser(__doc__.strip())

    parser.add_option('--debug', action='store_true',
                      help="Debugging output.")

    parser.add_option('-I', '--ignore', dest='ignores', action='append',
                      default=def_ignores,
                      help="Add the given directory name to the list to be ignored.")

    parser.add_option('-d', '--duplicates', '--enable-duplicates',
                      dest='do_dups', action='store_true',
                      help="Enable experimental heuristic for finding duplicate imports.")

    parser.add_option('-m', '--missing', '--enable-missing',
                      dest='do_missing', action='store_true',
                      help="Enable experimental heuristic for finding missing imports.")

    opts, args = parser.parse_args()

    write = sys.stderr.write
    for fn in iter_pyfiles(args or ['.'], opts.ignores, False):

        # Parse the file.
        found_imports, ast, lines = parse_python_source(fn)

        # Check for duplicate remote names imported.
        if opts.do_dups:
            found_imports, dups = check_duplicate_imports(found_imports)
            for modname, rname, lname, lineno, pragma in dups:
                write("%s:%d:  Duplicate import '%s'\n" % (fn, lineno, lname))

        # Filter out the unused imports.
        used_imports, unused_imports = filter_unused_imports(ast, found_imports)

        # Output warnings for the unused imports.
        for x in unused_imports:
            _, _, lname, lineno, _ = x
            # Search for the column in the relevant line.
            mo = re.search(r'\b%s\b' % lname, lines[lineno-1])
            colno = mo.start()+1 if mo else 0
            write("%s:%d:%d:  Unused import '%s'\n" % (fn, lineno, colno, lname))

        # (Optionally) Compute the list of names that are being assigned to.
        if opts.do_missing or opts.debug:
            vis = AssignVisitor()
            compiler.walk(ast, vis)
            assign_names = vis.finalize()

        # (Optionally) Check for potentially missing imports (this cannot be
        # precise, we are only providing a heuristic here).
        if opts.do_missing:
            defined = set(modname for modname, _, _, _, _ in used_imports)
            defined.update(x[0] for x in assign_names)
            for name, lineno in simple_names:
                if name not in defined and name not in __builtin__.__dict__:
                    write("%s:%d:  Missing import for '%s'\n" % (fn, lineno, name))

        # Print out all the schmoo for debugging.
        if opts.debug:
            print
            print
            print '------ Imported names:'
            for modname, rname, lname, lineno, pragma in found_imports:
                print '%s:%d:  %s' % (fn, lineno, lname)

            print
            print
            print '------ Exported names:'
            for name, lineno in exported:
                print '%s:%d:  %s' % (fn, lineno, name)

            print
            print
            print '------ Used names:'
            for name, lineno in dotted_names:
                print '%s:%d:  %s' % (fn, lineno, name)
            print

            print
            print
            print '------ Assigned names:'
            for name, lineno in assign_names:
                print '%s:%d:  %s' % (fn, lineno, name)

            print
            print
            print '------ AST:'
            printAst(ast, indent='    ', stream=sys.stdout, initlevel=1)
            print



def filter_unused_imports(ast, found_imports):
    """
    Given the ast and the list of found imports in the file, find out which of
    the imports are not used and return two lists: a list of used imports, and a
    list of unused imports.
    """
    used_imports, unused_imports = [], []

    # Find all the names being referenced/used.
    vis = NamesVisitor()
    compiler.walk(ast, vis)
    dotted_names, simple_names = vis.finalize()

    # Find all the names being exported via __all__.
    vis = AllVisitor()
    compiler.walk(ast, vis)
    exported = vis.finalize()

    # Check that all imports have been referenced at least once.
    usednames = set(x[0] for x in dotted_names)
    usednames.update(x[0] for x in exported)
    used_imports = []
    for x in found_imports:
        _, _, lname, lineno, _ = x
        if lname not in usednames:
            unused_imports.append(x)
        else:
            used_imports.append(x)

    return used_imports, unused_imports


class Visitor(object):
    "Base class for our visitors."
    def continue_(self, node):
        for child in node.getChildNodes():
            self.visit(child)


class NamesVisitor(Visitor):
    """AST visitor that finds all the identifier references that are defined,
    including dotted references. This includes all free names and names with
    attribute references.
    """
    def __init__(self):
        self.dotted = []
        self.simple = []
        self.attributes = []

    def visitName(self, node):
        self.attributes.append(node.name)
        self.attributes.reverse()
        attribs = self.attributes
        for i in xrange(1, len(attribs)+1):
            self.dotted.append(('.'.join(attribs[0:i]), node.lineno))
        self.simple.append((attribs[0], node.lineno))
        self.attributes = []

    def visitGetattr(self, node):
        self.attributes.append(node.attrname)
        self.continue_(node)

    def finalize(self):
        return self.dotted, self.simple


class AssignVisitor(Visitor):
    """AST visitor that builds a list of all potential names that are being
    assigned to. This is used later to heuristically figure out if a name being
    refered to is never assigned to nor in the imports."""

    def __init__(self):
        self.assnames = []
        self.in_class = False

    def visitAssName(self, node):
        self.assnames.append((node.name, node.lineno))
        self.continue_(node)

    def visitClass(self, node):
        self.assnames.append((node.name, node.lineno))
        prev, self.in_class = self.in_class, True
        self.continue_(node)
        self.in_class = prev

    def visitFunction(self, node):
        # Avoid method definitions.
        if not self.in_class:
            self.assnames.append((node.name, node.lineno))
        self.continue_(node)

    def finalize(self):
        return self.assnames


class AllVisitor(Visitor):
    """AST visitor that find an __all__ directive and accumulates the list of
    constants in it."""

    def __init__(self):
        self.all = []
        self.in_assign = False
        self.in_all = False

    def visitAssign(self, node):
        prev, self.in_assign = self.in_assign, True
        self.continue_(node)
        self.in_assign = prev

    def visitAssName(self, node):
        if self.in_assign and node.name == '__all__':
            self.in_all = True
        self.continue_(node)

    def visitConst(self, node):
        if self.in_assign and self.in_all:
            self.all.append((node.value, node.lineno))
        self.continue_(node)

    def finalize(self):
        return self.all


if __name__ == '__main__':
    main()
    # For tests, see snakefood/test/snakefood.


