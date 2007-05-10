# Run the automated tests.

.SUFFIXES: .py .deps .log


TARGETS =					\
	simple/stdlib				\
	simple/invalid				\
	simple/notfound				\
	project/foo_import			\
	project/foo_from

all: $(TARGETS)

# Check the standard library.
simple/stdlib simple/invalid simple/notfound:
	snakefood $@.py > $@.deps 2> $@.log
	diff $@.deps $@.expect

project/foo_import project/foo_from:
	snakefood $@.py > $@.deps 2> $@.log
	diff $@.deps $@.expect

clean:
	rm -f *.deps *.log

