# Graph the dependencies for GNU Mailman

ROOT=$(HOME)/src/mailman-2.1.9/Mailman

PDFS =						\
	mailman.pdf

include ../Makefile.rules

# Cluster the subdirectories.
mailman.clusters:
	(cd $(ROOT)/..; ls -1d Mailman/* | grep -v \\.) > $(shell pwd)/$@


