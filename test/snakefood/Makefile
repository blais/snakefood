# Run the automated tests.

.SUFFIXES: .py .deps .log


TARGETS = 					\
	simple/stdlib 				\
	simple/invalid				\
	simple/relative				\
	simple/notfound

all: $(TARGETS)

# Check the standard library.
simple/stdlib:
	snakefood $@.py > $@.deps 2> $@.log
	diff $@.deps $@.expect

simple/invalid:
	snakefood $@.py > $@.deps 2> $@.log
	diff $@.deps $@.expect

simple/notfound:
	snakefood $@.py > $@.deps 2> $@.log
	diff $@.deps $@.expect

simple/relative:
	snakefood project/foo_*.py > $@.deps 2> $@.log
	diff $@.deps $@.expect

clean:
	rm -f *.deps *.log

