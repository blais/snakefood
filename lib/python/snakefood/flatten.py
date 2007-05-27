"""
Read a snakefood dependencies file and flatten and output the list of all files.
"""

import sys, os
from os.path import join

from depends import read_depends, flatten_depends



def main():
    import optparse
    parser = optparse.OptionParser(__doc__.strip())
    opts, args = parser.parse_args()

    depends = read_depends(sys.stdin)
    for droot, drel in flatten_depends(depends):
        print join(droot, drel)

