# Run the automated tests.

.SUFFIXES: .py .deps .log


all: stdlib invalid relative notfound


# Check the standard library.
stdlib:
	snakefood $@.py > $@.deps 2> $@.log
	diff $@.deps $@.expect

invalid:
	snakefood $@.py > $@.deps 2> $@.log
	diff $@.deps $@.expect

notfound:
	snakefood $@.py > $@.deps 2> $@.log
	diff $@.deps $@.expect

relative:
	snakefood project/foo_*.py > $@.deps 2> $@.log
	diff $@.deps $@.expect

clean:
	rm -f *.deps *.log

