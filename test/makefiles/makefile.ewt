# Compute the dependencies for the EWT codebase.

ROOT=$(HOME)/p/diamond

all: diamond.pdf

diamond.deps.raw:
	snakefood $(ROOT)/src > diamond.deps.raw

diamond.pdf: diamond.deps.raw
	cd $(ROOT)/src; ls -1d */* | grep -v .py > clusters
	cat diamond.deps.raw | grep -v /usr/lib/python2. | snakefood-cluster -f clusters > diamond.deps.clean
	cat diamond.deps.clean | snakefood-graph -e | dot -Tps | ps2pdf - > diamond.pdf

