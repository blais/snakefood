# Graph the dependencies for zooko's pyutil.

ROOT=/usr/lib/python2.5

PDFS =						\
	stdlib.pdf

include ../Makefile.rules

# Remove anything that is not simply from the root of the package dir (including
# site-packages).
stdlib.deps: raw.deps
	cat $< | grep -v "$(ROOT)/" > $@

# Cluster at least the first level of subdirectories.
stdlib.clusters: 
	(cd $(ROOT); ls -1d * | grep -v \\. > $(shell pwd)/$@)

# FIXME: we could try clustering a variety of modules by hand, according to the
# documentation groupings, but that would require supporting cluster groups that
# do not depend on a filename prefix.  Do that and then run this again.
