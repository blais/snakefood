# Graph the dependencies for SQLObject.

ROOT=$(HOME)/src/SQLObject

PDFS =						\
	sqlobject.pdf
# 	sqlobject-simple.pdf

include ../Makefile.rules

sqlobject.deps: raw.deps
	cat $< | grep -v /test > $@

