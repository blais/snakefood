"""
Parse Python files and output a unified list of imported symbols.

The imported modules/symbols are output even if they cannot be found.  (You
could try to do this with grep, but this is more accurate because it uses the
AST to obtain the list of imports.)

See http://furius.ca/snakefood for details.
"""

import sys, os, logging, traceback, re
import imp, compiler
from os.path import *
from collections import defaultdict
from operator import itemgetter
from dircache import listdir


class ImportVisitor(object):
    "AST visitor for grabbing the import statements."

    def __init__(self):
        self.modules = []

    def visitImport(self, node):
        self.modules.extend((x[0], None, node.lineno) for x in node.names)

    def visitFrom(self, node):
        modname = node.modname
        for name, as_ in node.names:
            if name != '*':
                mod = (modname, name, node.lineno)
            else:
                mod = (modname, None, node.lineno)
            self.modules.append(mod)


def process_file(fn, verbose):
    "Returns a list of the files it depends on."
    file_errors = []

    try:
        mod = compiler.parseFile(fn)
    except Exception, e:
        logging.error("Error processing file '%s':\n\n%s" %
                      (fn, traceback.format_exc(sys.stderr)))
        return [], file_errors

    vis = ImportVisitor()
    compiler.walk(mod, vis)

    symnames = []
    dn = dirname(fn)

    packroot = None
    for modname, name, lineno in vis.modules:
        islocal = False
        names = modname.split('.')
        if find_dotted(names, dn):
            # This is a local import, we need to find the root in order to
            # compute the absolute module name.
            if packroot is None:
                packroot = find_package_root(fn)
                if not packroot:
                    logging.warning(
                        "%d: Could not find package root for local import '%s' from '%s'." %
                        (lineno, modname, fn))
                    continue

            reldir = dirname(fn)[len(packroot)+1:]

            modname = '%s.%s' % (reldir.replace(os.sep, '.'), modname)
            islocal = True

        if name is not None:
            modname = '%s.%s' % (modname, name)
        symnames.append( (modname, lineno, islocal) )

    return symnames

def find_package_root(dn):
    "Search up the directory tree for a package root."
    if not isdir(dn):
        dn = dirname(dn)
    while is_package_dir(dn):
        assert dn
        dn = dirname(dn)
    if dn and is_package_root(dn):
        return dn

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

try:
    from imp import ImpImporter
except ImportError:
    from pkgutil import ImpImporter

def find_dotted(names, parentdir=None):
    """
    Dotted import.  'names' is a list of path components, 'parentdir' is the
    parent directory.
    """
    filename = None
    for name in names:
        mod = ImpImporter(parentdir).find_module(name)
        if not mod:
            break
        filename = mod.get_filename()
        if not filename:
            break
        parentdir = dirname(filename)
    else:
        return filename

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


LOG_FORMAT = "%(levelname)-12s: %(message)s"

def main():
    import optparse
    parser = optparse.OptionParser(__doc__.strip())

    parser.add_option('-I', '--ignore', dest='ignores', action='append', default=[],
                      help="Add the given directory name to the list to be ignored.")

    parser.add_option('-u', '--unified', action='store_true',
                      help="Just output the unique set of dependencies found, "
                      "in no particular order, without the filenames.  The default "
                      "is to output all imports, in order of appearance, along with "
                      "the filename and line number.")

    parser.add_option('-v', '--verbose', action='count', default=0,
                      help="Output input lines as well.")

    opts, args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if opts.verbose >= 1 else logging.INFO,
                        format=LOG_FORMAT)
    if not args:
        logging.warning("Searching for files from root directory.")
        args = ['.']

    info = logging.info

    if opts.unified:
        all_symnames = set()
        for fn in iter_pyfiles(args, opts.ignores):
            all_symnames.update(x[0] for x in process_file(fn, opts.verbose))
        for symname in sorted(all_symnames):
            print symname
    else:
        for fn in iter_pyfiles(args, opts.ignores):
            if opts.verbose:
                lines = list(open(fn))
            for symname, lineno, islocal in process_file(fn, opts.verbose):
                print '%s:%d: %s' % (fn, lineno, symname)
                if opts.verbose:
                    for no in xrange(lineno-1, len(lines)):
                        l = lines[no].rstrip()
                        print '   %s' % l
                        if l[-1] != '\\':
                            break
                    print
                        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit("Interrupted.")

