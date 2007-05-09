# Compute the dependencies for the EWT codebase.

ROOT=$(HOME)/pe/diamond
GENGRAPH= snakefood-graph -p | dot -Tps | ps2pdf - 

all: diamond.pdf diamond.mt.pdf



# Generate the raw list of dependencies for the entire codebase.
diamond.raw.deps:
	snakefood $(ROOT)/src > diamond.raw.deps

# Only keep files imported at the root of diamond.
# This removes the stdlib files and the test subdirectories as well.
diamond.filtered.deps: diamond.raw.deps
	cat diamond.raw.deps | grep "$(ROOT)/src'.*$(ROOT)/src" > diamond.filtered.deps

# Cluster the files to remove unnecessary amount of detail.
clusters:
	(cd $(ROOT)/src; ls -1d */* | grep -v .py > $(shell pwd)/clusters)
diamond.clean.deps: diamond.filtered.deps clusters
	cat diamond.filtered.deps | snakefood-cluster -f clusters > diamond.clean.deps



#
# Generate the graphs.
#

# All of diamond.
diamond.pdf: diamond.clean.deps
	cat diamond.clean.deps | $(GENGRAPH) > diamond.pdf

# diamond without mtt.
diamond.mt.pdf: diamond.clean.deps
	cat diamond.clean.deps | grep -v mtt/ | $(GENGRAPH) > diamond.mt.pdf



clean:
	rm -f diamond.filtered.deps clusters diamond.clean.deps 
	rm -f *.pdf

realclean: clean
	rm -f diamond.raw.deps

