# !/usr/bin/python
# -*- coding: utf-8 -*-
"""runs all tests"""
import sys
import unittest

# Change PYTHONPATH to include dependencies.
sys.path.insert(0, '.')

import utils.dependencies  # pylint: disable=wrong-import-position


if __name__ == '__main__':
  dependency_helper = utils.dependencies.DependencyHelper()

  # TODO: Once mock is used in tests, use CheckTestDependencies().
  if not dependency_helper.CheckDependencies():
    sys.exit(1)
  test_suite = unittest.TestLoader().discover('tests', pattern='*.py')
  test_results = unittest.TextTestRunner(verbosity=2).run(test_suite)
  if not test_results.wasSuccessful():
    sys.exit(1)
