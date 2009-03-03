# Graph the dependencies for Scipy.

ROOT=$(HOME)/src/scipy/build/lib.linux-i686-2.5

PDFS =						\
	scipy.pdf

include ../Makefile.rules

scipy.clusters: 
	(cd $(ROOT); find scipy/* -type d ) > $(shell pwd)/$@

