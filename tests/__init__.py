from __future__ import unicode_literals

import gc
import platform
import unittest

try:
    # Python 3.3+
    from unittest import mock
except ImportError:
    # From PyPI
    import mock


def buffer_writer(string):
    """Creates a function that takes a ``buffer`` and ``buffer_size`` as the
    two last arguments and writes the given ``string`` to ``buffer``.
    """

    def func(*args):
        assert len(args) >= 2
        buffer_, buffer_size = args[-2:]

        # -1 to keep a char free for \0 terminating the string
        length = min(len(string), buffer_size - 1)

        # Due to Python 3 treating bytes as an array of ints, we have to
        # encode and copy chars one by one.
        for i in range(length):
            buffer_[i] = string[i].encode('utf-8')

        return len(string)

    return func


def gc_collect():
    """Run enough GC collections to make object finalizers run."""

    # XXX Tests of GC and cleanup behavior are generally flaky and icky,
    # especially when you target all of Python 2.7, 3.3+ and PyPy. Their result
    # quickly depends on other tests, the arguments to the test runner and the
    # computer running the tests. This skips them all for now.
    raise unittest.SkipTest

    if platform.python_implementation() == 'PyPy':
        # Since PyPy use garbage collection instead of reference counting
        # objects are not finalized before the next major GC collection.
        # Currently, the best way we have to ensure a major GC collection has
        # run is to call gc.collect() a number of times.
        [gc.collect() for _ in range(10)]
    else:
        gc.collect()