# Graph the dependencies for zooko's docutils.

ROOT=$(HOME)/src/docutils/docutils

PDFS =						\
	docutils.pdf

include ../Makefile.common


docutils.deps: docutils.clusters raw.deps
	cat raw.deps | grep -v test | snakefood-cluster -f $< > $@

docutils.clusters:
	( cd $(ROOT); find docutils/* -maxdepth 2 -type d | grep -v /.svn | sort -r ) > $(shell pwd)/$@


