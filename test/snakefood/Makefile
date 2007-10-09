# Run the automated tests.

.SUFFIXES: .py .deps .log .expect .roots


all: roots depends functional



# Tests comparing actual output with expected output.
TARGETS =					\
	simple/stdlib				\
	simple/invalid				\
	simple/notfound				\
	project/foo_import			\
	project/foo_from

CHECK =						\
	checker/notfound			\
	checker/simple				\
	checker/duplicate

FUNCTIONAL = 					\
	checker/test_checker

depends: $(TARGETS) $(CHECK) $(FUNCTIONAL)

functional: $(FUNCTIONAL)

$(TARGETS):
	@echo "------ Testing $@"
	@sfood $@.py > $@.deps 2> $@.log
	@diff $@.expect $@.deps



# Testing the root identification, against expect files.
TESTROOT = $(PWD)
RDIRS := $(shell find roots -type d | grep -v /.svn)
REXPECTS := $(RDIRS:=/.expect)
ROOTS = $(RDIRS:=/.roots)

roots: $(ROOTS)

.expect.roots:
	@echo "------ Testing root $@"
	sfood --print-roots $(dir $<) | sed -e "s@$(PWD)@@" > $@
	diff $< $@

genexpect: $(REXPECTS)

.PHONY: $(REXPECTS)
$(REXPECTS):
	@echo "------ Generating expect file for $@"
	sfood --print-roots $(dir $@) | sed -e "s@$(PWD)@@" > $@

viewroots:
	@for i in $(REXPECTS) ; do echo ; echo $$PWD/$$(dirname $$i) ; cat $$i ; done


$(CHECK):
	@echo "------ Testing $@"
	@sfood-checker $@.py > $@.log 2>&1
	@diff $@.expect $@.log

$(FUNCTIONAL):
	@echo "------ Functional test:" $@
	@python $@.py


clean:
	rm -f *.deps *.log {project,simple}/*.{deps,log}
	rm -f $(ROOTS)

