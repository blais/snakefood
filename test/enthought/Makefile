# Graph the dependencies for the Enthought Tool Suite.

ROOT=$(HOME)/p/enthought

PDFS =							\
	enthought.pdf					

# 	traits.pdf					\
# 	traits_simplified.pdf			

include ../Makefile.rules

# Old ETS, before the split.
# 
# ROOT=$(HOME)/p/enthought/src/lib
# 
# # Enthought, clustered.
# enthought.clusters:
# 	(cd $(ROOT); find enthought/* -mindepth 0 -maxdepth 0 -type d ! -name .svn > $(shell pwd)/$@)
# 
# # With more detail.
# enthought-big.clusters:
# 	(cd $(ROOT); find enthought/* -mindepth 1 -maxdepth 1 -type d ! -name .svn > $(shell pwd)/$@)

# New ETS, after split.


# Generate the raw list of dependencies for the entire codebase.
raw.deps: $(ROOT)
	sfood -v $(FOOD_FLAGS) $(ROOT)/enthought.* 2>&1 > $@ | tee raw.log

## enthought.deps: enthought.clusters raw.deps 
## 	cat raw.deps | grep enthought/ | grep -vE '(/usr/lib/python|examples|test|demo)' | sfood-cluster -f $< > $@

enthought.clusters:
	(cd $(ROOT); find * -mindepth 2 -maxdepth 2 -type d | \
	             grep -v /.svn | sed -e 's@[^/]*/@@') > $(shell pwd)/$@

# Just traits.
# We cluster traits differently, we want no details outside of traits, and lots inside.
traits.clusters: 
	(cd $(ROOT); \
	find enthought -mindepth 1 -maxdepth 1 -type d ! -name .svn ; \
	find enthought/traits -mindepth 1 -maxdepth 1 -type d ! -name .svn ; ) > $(shell pwd)/$@

traits_simplified.deps: traits.deps
	cat $< | grep enthought/traits > $@



