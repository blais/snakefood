# Compute the dependencies for the Enthought Tool Suite.

ROOT=$(HOME)/p/enthought/src/lib
GENGRAPH= dot -Tps | ps2pdf - 

PDFS= 	enthought.pdf				\
	traits_full.pdf				\
	traits_simple.pdf			\

all: $(PDFS)



# Generate the raw list of dependencies for the entire codebase.
enthought.raw.deps:
	snakefood $(ROOT) > enthought.raw.deps

# Only keep files imported at the root of enthought.
# This removes the stdlib files and the test subdirectories as well.
enthought.filtered.deps: enthought.raw.deps
	cat enthought.raw.deps | grep "$(ROOT)'.*$(ROOT)" > enthought.filtered.deps

# Cluster the files to remove unnecessary amount of detail.
clusters:
	(cd $(ROOT); find enthought/* -mindepth 1 -maxdepth 1 -type d ! -name .svn > $(shell pwd)/clusters)
enthought.clean.deps: enthought.filtered.deps clusters
	cat enthought.filtered.deps | snakefood-cluster -f clusters > enthought.clean.deps



#
# Generate the graphs.
#

# All of enthought.
enthought.pdf: enthought.clean.deps
	cat enthought.clean.deps | snakefood-graph -p | $(GENGRAPH) > enthought.pdf

# Just traits.
# We cluster traits differently, we want no details outside of traits, and lots inside.
clusters.traits: clusters
	(cd $(ROOT); \
	find enthought -mindepth 1 -maxdepth 1 -type d ! -name .svn ; \
	find enthought/traits -mindepth 1 -maxdepth 1 -type d ! -name .svn ; ) > $(shell pwd)/clusters.traits

traits.deps: enthought.filtered.deps
	cat enthought.filtered.deps | snakefood-cluster -f clusters.traits > traits.deps

traits_simple.pdf: traits.deps
	cat traits.deps | grep enthought/traits | snakefood-graph -p | $(GENGRAPH) > traits_simple.pdf
traits_full.pdf: traits.deps
	cat traits.deps | snakefood-graph -p | $(GENGRAPH) > traits_full.pdf




clean:
	rm -f enthought.filtered.deps clusters enthought.clean.deps 
	rm -f *.pdf

realclean: clean
	rm -f enthought.raw.deps


