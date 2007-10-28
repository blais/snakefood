"""Code for checking for local names and superfluous import statements.

This script is used to detect forgotten imports that are not used anymore. When
writing Python code (which happens so fast), it is often the case that we forget
to remove useless imports.

This is implemented using a search in the AST, and as such we do not require to
import the module in order to run the checks. This is a major advantage over all
the other lint/checker programs, and the main reason for taking the time to
write it.
"""
# This file is part of the Snakefood open source package.
# See http://furius.ca/snakefood/ for licensing details.

# stdlib imports
import sys, __builtin__, re
from os.path import *
import compiler

from snakefood.util import def_ignores, iter_pyfiles
from snakefood.find import parse_python_source, check_duplicate_imports
from snakefood.astpretty import printAst

__all__ = ('filter_unused_imports', 'NamesVisitor', 'AssignVisitor', 'AllVisitor')



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


