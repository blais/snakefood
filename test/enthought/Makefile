# Graph the dependencies for the Enthought Tool Suite.

ROOT=$(HOME)/p/enthought/src/lib

PDFS =							\
	enthought.pdf					\
	enthought-big.pdf				\
	traits.pdf					\
	traits_simplified.pdf			

include ../Makefile.rules

# Enthought, clustered.
enthought.clusters:
	(cd $(ROOT); find enthought/* -mindepth 0 -maxdepth 0 -type d ! -name .svn > $(shell pwd)/$@)

# With more detail.
enthought-big.clusters:
	(cd $(ROOT); find enthought/* -mindepth 1 -maxdepth 1 -type d ! -name .svn > $(shell pwd)/$@)

# Just traits.
# We cluster traits differently, we want no details outside of traits, and lots inside.
traits.clusters: 
	(cd $(ROOT); \
	find enthought -mindepth 1 -maxdepth 1 -type d ! -name .svn ; \
	find enthought/traits -mindepth 1 -maxdepth 1 -type d ! -name .svn ; ) > $(shell pwd)/$@

traits_simplified.deps: traits.deps
	cat $< | grep enthought/traits > $@



