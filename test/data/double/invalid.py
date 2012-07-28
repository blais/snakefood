#!/usr/bin/env python

class printtest():
    """
    This is an improperly formated doctest
    """
    >>> import os
    >>> import sys
    # >>> from a.b import c3
    # 
    # >>> import x.y.z1
    print "This is a doctest"

if __name__ == "__main__":                                                                                                                                                                                  
    import doctest
    doctest.testmod()
