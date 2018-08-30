# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the plaso sqlite scaffolder."""
import unittest

from plasoscaffolder.lib import errors
from plasoscaffolder.scaffolders import plaso_sqlite


class PlasoSqliteScaffolderTest(unittest.TestCase):
  """Test class for the plaso sqlite scaffolder."""

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

    self.assertFalse(True)



if __name__ == '__main__':
  unittest.main()
