# Graph the dependencies for Python Web Objects.
include ../Makefile.common

ROOT=$(HOME)/src/PythonWeb.org

PDFS =						\
	pythonweb.pdf


# Cluster at least the first level of subdirectories.
pythonweb.clusters:
	(cd $(ROOT); \
	echo scripts > $(shell pwd)/$@ ; \
	ls -1d web/* | grep -v \\. >> $(shell pwd)/$@)


