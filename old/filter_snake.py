#!/usr/bin/python
import sys
from snakefood.depends import read_depends

## def read_depends(f):
##     "Generator for the dependencies read from the given file object."
##     for line in f:
##         try:
##             yield eval(line)
##         except Exception:
##             logging.warning("Invalid line: '%s'" % line)

depends = read_depends (sys.stdin)

for d in depends:

    if (d[0][0].startswith ('/home/nbecker/idma-cdma') and \
        (d[1][0] == None or \
         d[1][0].startswith ('/home/nbecker/idma-cdma'))):
        print d
