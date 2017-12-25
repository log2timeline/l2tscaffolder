# !/usr/bin/python
# -*- coding: utf-8 -*-
"""testing the main"""
import unittest
from unittest.mock import patch

from click.testing import CliRunner
from plasoscaffolder.frontend import main


class MainTest(unittest.TestCase):
  """the main test"""

  def testMainHelp(self):
    """testing the help of the main"""
    runner = CliRunner()
    result = runner.invoke(main.entry_point, ['--help'])
    expected_output = ('Usage: entry_point [OPTIONS] COMMAND [ARGS]...\n'
                       '\n'
                       'Options:\n'
                       '  --help  Show this message and exit.\n'
                       '\n'
                       'Commands:''\n'
                       '  sqlite\n')

    self.assertEqual(expected_output, str(result.output))
    self.assertEqual(0, result.exit_code)

  def testSQLiteHelp(self):
    """testing the main of the sqlite"""
    runner = CliRunner()
    result = runner.invoke(main.entry_point, ['sqlite', '--help'])
    expected_output = ('Usage: entry_point sqlite [OPTIONS]\n'
                       '\n'
                       'Options:\n'
                       '  --path TEXT       The path to plaso\n'
                       '  --name TEXT       The plugin name\n'
                       '  --testfile TEXT   The testfile path\n'
                       '  --sql / --no-sql  The output example flag for the '
                       'SQL Query for the plugin.\n'
                       '  --help            Show this message and exit.\n')

    self.assertEqual(expected_output, str(result.output))
    self.assertEqual(0, result.exit_code)

  @patch('plasoscaffolder.frontend.main.entry_point', return_value='run sqlite')
  def testSQLiteRun(self, sqlite): #pylint: disable=unused-argument
    """testing the interaction with main and sqlite"""
    runner = CliRunner()
    result = runner.invoke(main.entry_point, ['sqlite'])
    self.assertEqual(0, result.exit_code)
    self.assertIsNone(result.exception)
    self.assertIsNone(result.exc_info)


if __name__ == '__main__':
  unittest.main()
