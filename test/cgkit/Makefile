# Graph the dependencies for cgkit.

ROOT=$(HOME)/src/cgkit/build/lib.linux-i686-2.5

PDFS =						\
	cgkit.pdf

include ../Makefile.rules

# No clusters.
cgkit.clusters: $(ROOT)
	(cd $(ROOT); find cgkit -type d | sort -nr) > $(shell pwd)/$@

cgkit.deps: cgkit.clusters raw.deps
	cat raw.deps | grep -v cgkit/all | sfood-cluster -f $< > $@

