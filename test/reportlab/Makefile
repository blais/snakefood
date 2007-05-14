# Graph the dependencies for GNU Reportlab

ROOT=$(HOME)/src/reportlab_2_0

PDFS =						\
	reportlab.pdf

include ../Makefile.rules


# Cluster the subdirectories.
reportlab.clusters:
	(cd $(ROOT); ls -1d reportlab/*/* ; ls -1d reportlab/*) | grep -v \\. > $(shell pwd)/$@

