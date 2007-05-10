# Graph the dependencies for Twisted Matrix.
include ../Makefile.common

ROOT=$(HOME)/src/Twisted

PDFS =						\
	twisted.pdf


# Cluster at least the first level of subdirectories.
twisted.clusters:
	(cd $(ROOT); ls -1d twisted/* | grep -v \\. > $(shell pwd)/$@)


