# Run the automated tests.

.SUFFIXES: .py .deps .log .expect .roots


all: roots depends



# Tests comparing actual output with expected output.
TARGETS =					\
	simple/stdlib				\
	simple/invalid				\
	simple/notfound				\
	project/foo_import			\
	project/foo_from

depends: $(TARGETS)

$(TARGETS):
	@echo "Testing $@"
	@snakefood $@.py > $@.deps 2> $@.log
	@diff $@.expect $@.deps



# Testing the root identification, against expect files.
REXPECTS := $(shell find roots -name '*.expect')
ROOTS = $(REXPECTS:.expect=.roots)

TESTROOT = $(PWD)

roots: $(ROOTS)

.expect.roots:
	@echo "-- Testing root $@"
	snakefood --print-roots $(dir $<) | sed -e "s@$(PWD)@@" > $@
	diff $< $@

genexpect: $(REXPECTS)

.PHONY: $(REXPECTS)
$(REXPECTS):
	@echo "-- Generating expect file for $@"
	snakefood --print-roots $(dir $@) | sed -e "s@$(PWD)@@" > $@

viewroots:
	@for i in $(REXPECTS) ; do echo ; echo $$PWD/$$(dirname $$i) ; cat $$i ; done



clean:
	rm -f *.deps *.log
	rm -f $(ROOTS)

