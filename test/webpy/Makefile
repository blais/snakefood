# Graph the dependencies for SQLObject.

ROOT=$(HOME)/src/webpy/web

PDFS =						\
	webpy.pdf

include ../Makefile.rules

webpy.deps: raw.deps
	cat $< | grep -v /test > $@

