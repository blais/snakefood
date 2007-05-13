# Graph the dependencies for Python Web Objects.

ROOT=$(HOME)/src/PythonWeb.org

PDFS =						\
	pythonweb.pdf

include ../Makefile.rules

# Cluster at least the first level of subdirectories.
pythonweb.clusters:
	(cd $(ROOT); \
	echo scripts > $(shell pwd)/$@ ; \
	ls -1d web/* | grep -v \\. >> $(shell pwd)/$@)


