# Run the automated tests.

.SUFFIXES: .py .deps .log




# Check the standard library.
stdlib:
	snakefood $@.py > $@.deps 2> $@.log
	diff $@.deps $@.expect

invalid:
	snakefood $@.py > $@.deps 2> $@.log
	diff $@.deps $@.expect

clean:
	rm -f *.deps *.log
