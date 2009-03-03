# Graph the dependencies for Twisted Matrix.

ROOT=/usr/lib/python2.5/site-packages/twisted

PDFS =						\
	twisted.pdf

include ../Makefile.rules

# Cluster at least the first level of subdirectories.
twisted.clusters:
	(cd $(ROOT)/..; ls -1d twisted/* | grep -v \\. > $(shell pwd)/$@)


