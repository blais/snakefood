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
from dircache import listdir

from find import find_imports
from util import iter_pyfiles, is_python
from roots import find_package_root, is_package_dir, is_package_root





LOG_FORMAT = "%(levelname)-12s: %(message)s"

def list_imports():
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
                        

def main():
    try:
        list_imports()
    except KeyboardInterrupt:
        raise SystemExit("Interrupted.")


