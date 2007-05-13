# Run the automated tests.

.SUFFIXES: .py .deps .log


TARGETS =					\
	simple/stdlib				\
	simple/invalid				\
	simple/notfound				\
	project/foo_import			\
	project/foo_from

all: $(TARGETS)

simple/stdlib simple/invalid simple/notfound project/foo_import project/foo_from:
	@echo "Testing $@"
	@snakefood $@.py > $@.deps 2> $@.log
	@diff $@.expect $@.deps

clean:
	rm -f *.deps *.log

