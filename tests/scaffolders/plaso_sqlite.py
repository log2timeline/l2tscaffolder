# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the plaso sqlite scaffolder."""
import unittest

from l2tscaffolder.lib import errors
from l2tscaffolder.scaffolders import plaso_sqlite


class PlasoSQLiteScaffolderTest(unittest.TestCase):
  """Test class for the plaso sqlite scaffolder."""

  maxDiff = None

  def _RunQueryTests(self, scaffolder, test_string, expected_columns):
    """Test query columns function.

    Args:
      scaffolder (plaso_sqlite.PlasoSQLiteScaffolder): scaffolder to test.
      test_string (str): string to test the _GetQueryColumns method on.
      expected_columns (set[str]): columns names expected to be extracted from
          the test string.
    """
    # pylint: disable=protected-access
    columns = set(list(scaffolder._GetQueryColumns(test_string)))
    self.assertEqual(columns, expected_columns)

  def testQueryColumns(self):
    """Test query columns function."""
    scaffolder = plaso_sqlite.PlasoSQLiteScaffolder()
    test_string = (
        'SELECT foobar as Foo, foobar.dot, random, reallylong AS long FROM '
        'foobarengine WHERE foobar = 1')
    expected_columns = set(['foo', 'dot', 'random', 'long'])
    self._RunQueryTests(scaffolder, test_string, expected_columns)

    test_string = (
        'select one, two as three, four as five, f.eight as EIGHTE FROM '
        'foobar f, scode s WHERE f.id = s.id ORDER BY one')
    expected_columns = set(['one', 'three', 'five', 'eighte'])
    self._RunQueryTests(scaffolder, test_string, expected_columns)

    test_string = (
        'this should not produce anything...')
    self._RunQueryTests(scaffolder, test_string, set())

  def testPlasoSQLiteScaffolder(self):
    """Test the plaso SQLite scaffolder."""
    scaffolder = plaso_sqlite.PlasoSQLiteScaffolder()

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

    file_copy_paths = [x for _, x in scaffolder.GetFilesToCopy()]
    self.assertEqual(file_copy_paths, ['test_data/test_sqlite.db'])

    files_generated = dict(scaffolder.GenerateFiles())

    expected_files = frozenset([
        'plaso/formatters/testing.py', 'tests/formatters/testing.py',
        'plaso/parsers/sqlite_plugins/testing.py',
        'tests/parsers/sqlite_plugins/testing.py'])
    self.assertEqual(set(files_generated.keys()), expected_files)

    expected_init_files = frozenset([
        'plaso/formatters/__init__.py',
        'plaso/parsers/sqlite_plugins/__init__.py'])
    init_generated = dict(scaffolder.GetInitFileChanges())
    self.assertEqual(set(init_generated.keys()), expected_init_files)

    expected_parser_init_addition = (
        'from '
        'plaso.parsers.sqlite_plugins import testing\n')
    self.assertEqual(
        expected_parser_init_addition,
        init_generated['plaso/parsers/sqlite_plugins/__init__.py'])

    with open('test_data/plaso_testing_sqlite_plugin.py', 'r') as fh:
      expected_parser_content = fh.read()
    self.assertEqual(
        expected_parser_content,
        files_generated['plaso/parsers/sqlite_plugins/testing.py'])


if __name__ == '__main__':
  unittest.main()
