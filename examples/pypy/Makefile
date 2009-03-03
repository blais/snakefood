# Graph the dependencies for PyPy/Pylib.

ROOT=$(HOME)/src/pypy-dist

PDFS =						\
	pypy.pdf

include ../Makefile.rules

# Cluster at least the first level of subdirectories.
pypy.clusters:
	(cd $(ROOT); ls -1d py/* pypy/* | grep -v \\. ) > $(shell pwd)/$@


