# Compute the dependencies for the EWT codebase.

ROOT=$(HOME)/src/Gnosis_Utils-1.2.1
GENGRAPH= snakefood-graph -p | dot -Tps | ps2pdf - 

all: gnosis.pdf 



# Generate the raw list of dependencies for the entire codebase.
gnosis.raw.deps:
	snakefood $(ROOT) > gnosis.raw.deps

# Only keep files imported at the root of gnosis.
# This removes the stdlib files and the test subdirectories as well.
gnosis.filtered.deps: gnosis.raw.deps
	cat gnosis.raw.deps | grep "$(ROOT)'.*$(ROOT)" > gnosis.filtered.deps

# Cluster the files to remove unnecessary amount of detail.
gnosis.clean.deps: gnosis.filtered.deps clusters
	cat gnosis.filtered.deps | snakefood-cluster -f clusters > gnosis.clean.deps



#
# Generate the graphs.
#

# All of gnosis.
gnosis.pdf: gnosis.clean.deps
	cat gnosis.clean.deps | $(GENGRAPH) > gnosis.pdf



clean:
	rm -f gnosis.filtered.deps gnosis.clean.deps 
	rm -f *.pdf

realclean: clean
	rm -f gnosis.raw.deps

