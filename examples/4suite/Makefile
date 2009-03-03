# Graph the dependencies for 4suite-XML.

ROOT=$(HOME)/src/4Suite-XML-1.0.2/Ft

PDFS =						\
	4suite.pdf

include ../Makefile.rules

# Cluster all the packages.
4suite.clusters:
	(cd $(ROOT)/..; find Ft -type d | sort -r) > $(shell pwd)/$@


