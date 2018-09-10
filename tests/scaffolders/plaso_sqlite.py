# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the plaso sqlite scaffolder."""
import unittest

from plasoscaffolder.lib import errors
from plasoscaffolder.scaffolders import plaso_sqlite


class PlasoSqliteScaffolderTest(unittest.TestCase):
  """Test class for the plaso sqlite scaffolder."""

  maxDiff = None

  def testPlasoSqliteScaffolder(self):
    """Test the plaso sqlite scaffolder."""
    scaffolder = plaso_sqlite.PlasoSQliteScaffolder()

    scaffolder.SetupScaffolder()
    scaffolder.SetOutputName('testing')

    with self.assertRaises(errors.ScaffolderNotConfigured):
      scaffolder.RaiseIfNotReady()

    queries = {
        'strange': 'SELECT name, address, ssn FROM strange',
        'foobar': (
            'SELECT f1.foo, f2.bar AS Bar FROM foobar_one AS f1, '
            'foobar_two as f2 WHERE f1.id = f2.id')}
    required_tables = ['foobar_one', 'foobar_two', 'strange_table']
    scaffolder.SetAttribute('queries', queries, dict)
    scaffolder.SetAttribute('required_tables', required_tables, list)
    scaffolder.SetAttribute('test_file', 'test_data/test_sqlite.db', str)

    files_to_copy = [x for _, x in scaffolder.GetFilesToCopy()]
    self.assertEqual(files_to_copy, ['test_data/test_sqlite.db'])

    files_generated = {}
    for file_name, file_content in scaffolder.GenerateFiles():
      files_generated[file_name] = file_content

    expected_files = [
        'plaso/formatters/testing.py', 'tests/formatters/testing.py',
        'plaso/parsers/sqlite_plugins/testing.py',
        'tests/parsers/sqlite_plugins/testing.py',
        'plaso/formatters/__init__.py',
        'plaso/parsers/sqlite_plugins/__init__.py']
    self.assertSetEqual(set(files_generated.keys()), set(expected_files))

    expected_parser_init_addition = (
        '# TODO: put in alpha order.\nfrom '
        'plaso.parsers.sqlite_plugins import testing')
    self.assertEqual(
        expected_parser_init_addition, 
        files_generated['plaso/parsers/sqlite_plugins/__init__.py'])

    with open('test_data/plaso_testing_sqlite_plugin.py', 'r') as fh:
      expected_parser_content = fh.read()
    self.assertEqual(
        expected_parser_content,
        files_generated['plaso/parsers/sqlite_plugins/testing.py'])


if __name__ == '__main__':
  unittest.main()
