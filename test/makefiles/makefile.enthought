# Compute the dependencies for various Enthought libraries.

ROOT=$(HOME)/p/enthought
TMP=/tmp/deps
OUTPUT=$(HOME)/dependencies

all: $(OUTPUT) traits

$(OUTPUT):
	mkdir $(OUTPUT)

traits:
	snakefood --filter=$(ROOT)/src/lib $(ROOT)/src/lib/enthought/traits > $(TMP).traits.dot
	cat $(TMP).dot | grep -E -v "/(ui|examples|tests)/" | dot -Tps | ps2pdf - > $(OUTPUT)/traits.pdf

