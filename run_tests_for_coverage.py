# !/usr/bin/python
# -*- coding: utf-8 -*-
"""runs all tests"""
import sys
import unittest

if __name__ == '__main__':
  test_suite_bll = unittest.TestLoader().discover('tests.bll', pattern='*.py')
  test_suite_common = unittest.TestLoader().discover('tests.common',
                                                     pattern='*.py')
  test_suite_bll = unittest.TestLoader().discover('tests.bll', pattern='*.py')
  test_suite_dal = unittest.TestLoader().discover('tests.dal', pattern='*.py')
  test_suite_scaffolders = unittest.TestLoader().discover(
      'tests.scaffolders', pattern='*.py')
  test_suite_definitions = unittest.TestLoader().discover(
      'tests.definitions', pattern='*.py')
  test_suite_frontend = unittest.TestLoader().discover(
      'tests.frontend', pattern='*.py')
  test_suite_lib = unittest.TestLoader().discover(
      'tests.lib', pattern='*.py')
  test_suite_model = unittest.TestLoader().discover(
      'tests.model', pattern='*.py')
  test_suite_other = unittest.TestLoader().discover(
      'tests.other', pattern='*.py')
  all_tests = unittest.TestSuite((
    test_suite_bll, test_suite_common, test_suite_lib, test_suite_scaffolders,
    test_suite_dal, test_suite_frontend, test_suite_definitions,
    test_suite_model, test_suite_other))

  test_results = unittest.TextTestRunner(verbosity=2).run(all_tests)
  if not test_results.wasSuccessful():
    sys.exit(1)
