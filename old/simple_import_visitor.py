class SimpleImportVisitor(Visitor):
    """AST visitor that accumulates only the target names of import statements.
    This was originally used in sfood-checker."""
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
