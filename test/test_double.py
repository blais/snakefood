"""
Test using two dots in import syntax
Reporter: Dan Fayette (fayetted at gmail), on 2012-07-26

>>> Anyway, I found a problem where sfood-imports would choke on a
>>> unittest file (not named with a .py extension).
>>>
>>> in find.py I added this at line 93:
>>>     if ast is None:
>>>         return
>>>
>>> And that seems to have fixed the problem.  I still get the ERROR:Error
>>> processing file 'filename" line and the filename:line#: invalid syntax
>>> but it continues to parse through the project.
>>>
>>> The line in the unit test file that caused the problem was similar to this
>>>
>>>             import dir.dir.file
>>>
>>> I commented that line out and re-ran sfoods-import and it crashed on
>>> the next line that contained >>> import dir2.dir2.file2
"""

from __future__ import print_function

from os.path import *
from testsupport import *


def test_double():
    "Test that the root directories are being calculated correctly."

    fn = join(data, 'double/double.py')
    print('Testing for: %s' % fn)
    compare_expect(fn.replace('.py', '.expect'), None,
                   'sfood', fn, filterdir=(data, 'ROOT'))

    fn = join(data, 'double/invalid.py')
    print('Testing for: %s' % fn)
    compare_expect(fn.replace('.py', '.expect'), None,
                   'sfood', fn, filterdir=(data, 'ROOT'))
