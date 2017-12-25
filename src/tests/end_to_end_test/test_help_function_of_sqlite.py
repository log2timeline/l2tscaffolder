# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test Class for end to end Tests.
These Tests can only be run on Linux because it makes use of pexpect."""

import platform
import unittest

import pexpect
from tests.end_to_end_test import end_to_end_test_helper


class HelpFunctionOfSQLiteTest(unittest.TestCase):
  """Test file for help function for sqlite option."""

  def testHelpMessageForSQLitePlugin(self):
    """test the --help option for SQLite"""
    helper = end_to_end_test_helper.EndToEndTestHelper('not needed',
                                                       'not needed')

    if platform.system() in ['Linux']:
      message_help = (
          'Usage: main.py sqlite [OPTIONS]\r\n\r\n'
          'Options:\r\n  '
          '--path TEXT       The path to plaso\r\n  '
          '--name TEXT       The plugin name\r\n  '
          '--testfile TEXT   The testfile path\r\n  '
          '--sql / --no-sql  The output example flag for the SQL Query for the '
          'plugin.\r\n  '
          '--help            Show this message and exit.')

      command = 'python {0} sqlite --help'.format(helper.MAIN_PATH)
      child = pexpect.spawn(command)
      child.expect_exact(message_help)
    else:
      raise NotImplementedError("test only implemented for linux platform")


if __name__ == '__main__':
  unittest.main()
