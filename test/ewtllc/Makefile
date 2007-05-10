# Graph the dependencies for the EWT codebase.
include ../Makefile.common

ROOT=$(HOME)/p/diamond/src

PDFS =						\
	diamond.pdf				\
	diamond-mt.pdf				\
	diamond-core.pdf

# diamond, clustered.
diamond.clusters:
	(cd $(ROOT); ls -1d */* | grep -v \\. > $(shell pwd)/$@)

# Without mtt.
diamond-mt.deps: diamond.deps
	cat $< | grep -v mtt/ > $@

# With the core package exploded.
diamond-core.clusters: 
	(cd $(ROOT); ls -1d */* | grep -v \\. | grep -v /core > $(shell pwd)/$@)

