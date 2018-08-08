# !/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=protected-access
# because tests should access protected members
"""testing the dependencies"""
import unittest

from plasoscaffolder import dependencies


class DependenciesTest(unittest.TestCase):
  """the dependencies test"""

  def testDependencies(self):
    """testing that for each python dependencies there is a """
    python_keys = dependencies.PYTHON_DEPENDENCIES.keys()
    dpkg_keys = dependencies._DPKG_PACKAGE_NAMES.keys()
    pypi_keys = dependencies._PYPI_PROJECT_NAMES.keys()
    rpm_keys = dependencies._RPM_PACKAGE_NAMES.keys()
    python_test_keys = dependencies.PYTHON_TEST_DEPENDENCIES

    self.assertNotEqual(python_keys, [])
    self.assertEqual(python_keys, dpkg_keys)
    self.assertEqual(python_keys, pypi_keys)
    self.assertEqual(pypi_keys, rpm_keys)
    self.assertIsNotNone(python_test_keys)


if __name__ == '__main__':
  unittest.main()
