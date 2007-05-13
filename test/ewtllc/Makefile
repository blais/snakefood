# Graph the dependencies for the EWT codebase.

ROOT=$(HOME)/p/diamond/src

PDFS =						\
	diamond.pdf				\
	mt.pdf					\
	core.pdf				\
	apps.pdf

include ../Makefile.rules

# diamond, clustered.
diamond.clusters:
	(cd $(ROOT); ls -1d */* | grep -v \\. > $(shell pwd)/$@)

# Without mtt.
mt.deps: diamond.deps
	cat $< | grep -v mtt/ > $@

# With the core package exploded.
core.clusters: 
	(cd $(ROOT); ls -1d */* | grep -v \\. | grep -v /core > $(shell pwd)/$@)

apps.clusters:
	(cd $(ROOT); ls -1d mt/{gui,apps}/* | grep -v \\. ; echo mt ) > $(shell pwd)/$@
