# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test Class for end to end Tests.
These Tests can only be run on Linux because it makes use of pexpect."""

import platform
import unittest

import pexpect
from tests.end_to_end_test import end_to_end_test_helper


class HelpFunctionTest(unittest.TestCase):
  """Test file for help function"""

  def testHelpMessage(self):
    """test the universal --help Option"""
    helper = end_to_end_test_helper.EndToEndTestHelper('not needed',
                                                       'not needed')

    if platform.system() in ['Linux']:
      message_help = ('Usage: main.py [OPTIONS] COMMAND [ARGS]...\r\n\r\n'
                      'Options:\r\n'
                      '  --help  Show this message and exit.\r\n\r\n'
                      'Commands:\r\n'
                      '  sqlite')
      command = 'python {0} --help'.format(helper.MAIN_PATH)
      child = pexpect.spawn(command)
      child.expect_exact(message_help)
    else:
      raise NotImplementedError("test only implemented for linux platform")


if __name__ == '__main__':
  unittest.main()
