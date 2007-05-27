"""
Routines that manipulate, read and convert lists of dependencies.
"""

import sys
from operator import itemgetter


def output_depends(depdict):
    """Given a dictionary of (from -> list of targets), generate an appropriate
    output file."""

    # Output the dependencies.
    write = sys.stdout.write
    for (from_root, from_), targets in sorted(depdict.iteritems(),
                                             key=itemgetter(0)):
        for to_root, to_ in sorted(targets):
            write(repr( ((from_root, from_), (to_root, to_)) ))
            write('\n')

