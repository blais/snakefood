# Compute the dependencies for the Enthought Tool Suite.

ROOT=$(HOME)/p/enthought/src/lib/enthought
GENGRAPH= snakefood-graph -p | dot -Tps | ps2pdf - 

all: enthought.pdf



# Generate the raw list of dependencies for the entire codebase.
enthought.raw.deps:
	snakefood $(ROOT) > enthought.raw.deps

# Only keep files imported at the root of enthought.
# This removes the stdlib files and the test subdirectories as well.
enthought.filtered.deps: enthought.raw.deps
	cat enthought.raw.deps | grep "$(ROOT)/src'.*$(ROOT)/src" > enthought.filtered.deps

# Cluster the files to remove unnecessary amount of detail.
clusters:
	(cd $(ROOT); find */* -type d -maxdepth 1 ! -name .svn > $(shell pwd)/clusters)
enthought.clean.deps: enthought.filtered.deps clusters
	cat enthought.filtered.deps | snakefood-cluster -f clusters > enthought.clean.deps



#
# Generate the graphs.
#

# All of enthought.
enthought.pdf: enthought.clean.deps
	cat enthought.clean.deps | $(GENGRAPH) > enthought.pdf

# # Just traits.
# enthought.pdf: enthought.clean.deps
# 	cat enthought.clean.deps | $(GENGRAPH) > enthought.pdf


clean:
	rm -f enthought.filtered.deps clusters enthought.clean.deps 
	rm -f *.pdf

realclean: clean
	rm -f enthought.raw.deps

