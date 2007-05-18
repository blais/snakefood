# Run the automated tests.

.SUFFIXES: .py .deps .log

TARGETS =					\
	simple/stdlib				\
	simple/invalid				\
	simple/notfound				\
	project/foo_import			\
	project/foo_from

ROOTTESTS =					\
	roots

all: $(ROOTTESTS)
## all: $(TARGETS) $(ROOTTESTS)

$(TARGETS):
	@echo "Testing $@"
	@snakefood $@.py > $@.deps 2> $@.log
	@diff $@.expect $@.deps

FIXME contineue

.roots:
	@echo "Testing root $@"
	snakefood --print-roots > /tmp/roots
	@diff $<.expect

clean:
	rm -f *.deps *.log

