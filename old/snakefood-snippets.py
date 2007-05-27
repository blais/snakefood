# Conversion to filenames, this should work fine.

def depend_to_filename(dep):
    """Convert a dependency to a filename. 'dep' is expected to be a single pair
    of the form (dir, filename-or-dir)."""
    fn = join(*dep)
    if isdir(fn):
        fn = join(fn, '__init__.py')
    return fn

def depends_to_files(depends, do_from=True, do_to=True):
    """Convert dependencies to a set of files."""
    allfiles = set()
    for from_, to_ in depends:
        if do_from:
            allfiles.add(depend_to_filename(from_))
        if do_to and to_ != (None, None):
            allfiles.add(depend_to_filename(to_))

    return sorted(allfiles)





# Filtering code (use grep instead).


    parser.add_option('-f', '--filter', action='append', default=[],
                      help="Filter the results by include only the given path prefixes.")


def filter_p(opts, root, fn):
    "Return true if the file should be ignored."
    if not opts.filter:
        return False
    elif root in opts.filter_paths:
        return False
    else:
        return True


    # Apply filtering and name cleanup.
    depends = []
    for (from_root, from_), tolist in allfiles.iteritems():
        if filter_p(opts, from_root, from_):
            continue

        for (to_root, to_) in tolist:
            if filter_p(opts, to_root, to_):
                continue

            depends.append(((from_root, normpyfn(from_)),
                            (to_root, normpyfn(to_))))






# Clustering code (use sfood-cluster instead).


def apply_cluster(cdirs, root, fn):
    "If a cluster exists in 'cdirs' for the root/fn filename, reduce the filename."
    for croot, cfn in cdirs:
        if root == croot and fn.startswith(cfn):
            return root, cfn
    else:
        return root, fn  # no change.


    # Apply the clustering reduction rules.
    if opts.cluster_dirs:
        clusfiles = defaultdict(set)
        for (from_root, from_), tolist in allfiles.iteritems():
            for (to_root, to_) in tolist:
                cfrom_ = apply_cluster(opts.cluster_dirs, from_root, from_)
                cto_ = apply_cluster(opts.cluster_dirs, to_root, to_)
                clusfiles[cfrom_].add(cto_)
        allfiles = clusfiles






# Fancy output code.


    if lines:
        fmt = '%%-%ds ; //   %%s\n' % max(len(x[0]) for x in lines)
        for l, r in lines:
            write(fmt % (l, r))




Alternative format:

  Input:

        mo = re.match('([^,]*),([^;]*);([^,]*),(.*)', line)
        if not mo:
            logging.warning("Invalid line: '%s'" % line)
            continue
        yield (mo.group(1,2), mo.group(3,4))


  Output:

        for to_root, to_ in sorted(tolist):
            write('%s,%s;%s,%s\n' % (from_root, from_, to_root, to_))


