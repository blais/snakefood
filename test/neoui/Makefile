# Graph the dependencies for Python Web Objects.

ROOT=$(HOME)/src/piemenu/neoui.dev

PDFS =						\
	neoui.pdf				\
	piemenu.pdf

include ../Makefile.rules

# Cluster at least the first level of subdirectories.
neoui.clusters piemenu.clusters:
	(cd $(ROOT); \
	find . -type d | grep -v .bzr  | sort -r | cut -b3- ) > $(shell pwd)/$@

piemenu.deps: piemenu.clusters $(ROOT)
	sfood -v $(FOOD_FLAGS) --follow $(ROOT)/neoui/widgets/piemenu | sfood-cluster -f $< > $@


