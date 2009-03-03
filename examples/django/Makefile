# Graph the dependencies for Django.

ROOT=$(HOME)/src/django

PDFS =						\
	django.pdf				\
	django-simple.pdf

include ../Makefile.rules

# Cluster some of the directories.
django.clusters:
	(cd $(ROOT); ls -1d django/*/* | grep -v \\. > $(shell pwd)/$@)

django-simple.clusters:
	(cd $(ROOT); ls -1d django/* | grep -v \\. > $(shell pwd)/$@)

