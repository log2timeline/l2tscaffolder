# !/usr/bin/python
# -*- coding: utf-8 -*-
"""test class"""
import os
import unittest

from plasoscaffolder.dal import explain_query_plan
from plasoscaffolder.dal import sqlite_query_execution
from tests.test_helper import path_helper


class ExplainQueryPlanTest(unittest.TestCase):
  """test the SQLite Query execution test"""

  def setUp(self):
    database_path = path_helper.TestDatabasePath()
    file_path = os.path.join(database_path, 'twitter_ios.db')
    execute = sqlite_query_execution.SQLiteQueryExecution(file_path)
    execute.TryToConnect()
    self.explain_query_plan = explain_query_plan.ExplainQueryPlan(execute)

  def testIsReadOnlyIfTrue(self):
    """test IsReadOnly if it is True"""
    select_query = 'select id from users'
    result = self.explain_query_plan.IsReadOnly(select_query)
    self.assertTrue(result)

  def testIsReadOnlyIfFalseBecauseOfDrop(self):
    """test IsReadOnly if it is False because it is a drop query"""
    drop_query = 'drop table users'
    result = self.explain_query_plan.IsReadOnly(drop_query)
    self.assertFalse(result)

  def testIsReadOnlyIfFalseBecauseOfAlter(self):
    """test IsReadOnly if it is False because it is a alter query"""
    alter_query = 'alter table users rename users2'
    result = self.explain_query_plan.IsReadOnly(alter_query)
    self.assertFalse(result)

  def testIsReadOnlyIfFalseBecauseOfError(self):
    """test IsReadOnly with erroneous SQL query"""
    error_query = 'select bla from blub'
    result = self.explain_query_plan.IsReadOnly(error_query)
    self.assertFalse(result)

  def testIsReadOnlyIfFalseBecauseOfWarning(self):
    """test IsReadOnly with erroneous SQL query"""
    warning_query = 'select id from users;select id from users'
    result = self.explain_query_plan.IsReadOnly(warning_query)
    self.assertFalse(result)

if __name__ == '__main__':
  unittest.main()
