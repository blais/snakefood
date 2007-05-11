# Graph the dependencies for Numpy.

ROOT=$(HOME)/src/numpy

PDFS =						\
	numpy.pdf				\
	numpy-simple.pdf

include ../Makefile.common

numpy.deps: raw.deps
	cp $< $@

numpy-simple.deps: numpy-simple.clusters raw.deps
	cat raw.deps | grep -v test | snakefood-cluster -f $<  > $@

numpy-simple.clusters:
	( cd $(ROOT); find numpy -mindepth 1 -maxdepth 3 -type d | grep -v /.svn | sort -r ) > $(shell pwd)/$@

