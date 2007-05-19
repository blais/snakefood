# Run the automated tests.

.SUFFIXES: .py .deps .log .expect .roots

all: $(ROOTS)
## all: $(TARGETS)



# Tests comparing actual output with expected output.
TARGETS =					\
	simple/stdlib				\
	simple/invalid				\
	simple/notfound				\
	project/foo_import			\
	project/foo_from

$(TARGETS):
	@echo "Testing $@"
	@snakefood $@.py > $@.deps 2> $@.log
	@diff $@.expect $@.deps



# Testing the root identification, against expect files.
REXPECTS := $(shell find roots -name '*.expect')
ROOTS = $(REXPECTS:.expect=.roots)

.expect.roots:
	@echo "Testing root $@"
	snakefood --print-roots $(dir $<) > $@
	diff $< $@

viewroots:
	@for i in $(REXPECTS) ; do echo ; echo $$PWD/$$(dirname $$i) ; cat $$i ; done


clean:
	rm -f *.deps *.log
	rm $(ROOTS)
