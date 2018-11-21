# !/usr/bin/python
# -*- coding: utf-8 -*-
"""testing the main"""
import unittest

import plasoscaffolder


class VersionTest(unittest.TestCase):
  """the version in init test"""

  def testGetVersion(self):
    """testing the get version"""
    actual = plasoscaffolder.__version__
    self.assertEqual('20181120', actual)

if __name__ == '__main__':
  unittest.main()
