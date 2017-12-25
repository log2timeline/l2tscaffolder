# -*- coding: utf-8 -*-
"""test the commands for the sqlite plugin"""
import unittest

from click.testing import CliRunner
from plasoscaffolder.frontend.sqliteplugin import commands


class SqliteCommandsTest(unittest.TestCase):
  """testing the sqlite commands"""

  def testSqliteHelp(self):
    """testing the help argument"""
    runner = CliRunner()
    result = runner.invoke(commands.sqlite, ['--help'])
    expected_output = ('Usage: sqlite [OPTIONS]\n'
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
