# Graph the dependencies for my personal projects directory.

ROOT=$(PROJECTS)

PDFS = 						\
	projects.pdf

include ../Makefile.rules

raw.deps:
	sfood -i $(shell projects lsco -s | cut -d: -f1) | grep -v /test | grep -v /old > $(shell pwd)/$@

projects.clusters: $(ROOT)
	projects lsco -s | cut -d: -f2 | tr -d ' ' > $(shell pwd)/$@
	cat clusters >> $(shell pwd)/$@



