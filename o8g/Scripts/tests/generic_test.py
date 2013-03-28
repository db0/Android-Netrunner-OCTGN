#!/usr/bin/python

"""Test Suite for Android:Netrunner module of OCTGN

These tests can be run from the root directory of module with:
python -m scripts.tests.generic_test

There are variables in other modules initialized in OCTGN and thus unavailable
during unit testing. The RUNNING_TEST_SUITE environment variable is set here
and used in other modules to initialize those missing vars.

I suspect there might be another way to handle this, like initializing them
in main() of the test suite, but the current method is sufficient to run the
tests while ensuring these mock objects do not leak when OCTGN is running.
"""
import unittest
try:
    import os
    os.environ['RUNNING_TEST_SUITE'] = 'TRUE'
except ImportError:
    pass

from scripts import generic

class NumOrderTests(unittest.TestCase):

    def test_one_digit(self):
        """Test conversion of single digit ints to ordinals."""
        # These are correct conversions and should pass
        self.assertEqual('1st', generic.numOrder(0))
        self.assertEqual('2nd', generic.numOrder(1))
        self.assertEqual('3rd', generic.numOrder(2))
        self.assertEqual('4th', generic.numOrder(3))

        # These are incorrect conversions and should fail
        self.assertNotEqual('1st', generic.numOrder(1))

def main():
    unittest.main()

if __name__ == '__main__':
    main()