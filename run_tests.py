# !/usr/bin/python
# -*- coding: utf-8 -*-
"""runs all tests"""
import sys
import unittest

if __name__ == '__main__':
  test_suite_definitions = unittest.TestLoader().discover(
      'tests.definitions', pattern='*.py')
  test_suite_frontend = unittest.TestLoader().discover(
      'tests.frontend', pattern='*.py')
  # TODO: enable again once helper PR gets pushed in.
  #test_suite_helpers = unittest.TestLoader().discover(
  #    'tests.helpers', pattern='*.py')
  test_suite_lib = unittest.TestLoader().discover(
      'tests.lib', pattern='*.py')
  test_suite_scaffolders = unittest.TestLoader().discover(
      'tests.scaffolders', pattern='*.py')

  all_tests = unittest.TestSuite((
      test_suite_definitions, test_suite_frontend,# test_suite_helpers,
      test_suite_lib, test_suite_scaffolders))

  test_results = unittest.TextTestRunner(verbosity=2).run(all_tests)
  if not test_results.wasSuccessful():
    sys.exit(1)
