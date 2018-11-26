# !/usr/bin/python
# -*- coding: utf-8 -*-
"""testing the main"""
import unittest

import l2tscaffolder


class VersionTest(unittest.TestCase):
  """the version in init test"""

  def testGetVersion(self):
    """testing the get version"""
    actual = l2tscaffolder.__version__
    self.assertEqual('20181127', actual)


if __name__ == '__main__':
  unittest.main()
