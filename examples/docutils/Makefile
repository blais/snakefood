# Graph the dependencies for zooko's docutils.

ROOT=$(HOME)/src/docutils/docutils/docutils

PDFS =						\
	docutils.pdf

include ../Makefile.rules


docutils.clusters:
	( cd $(ROOT)/..; find docutils/* -maxdepth 2 -type d | grep -v /.svn | sort -r ) > $(shell pwd)/$@


