# !/usr/bin/python
# -*- coding: utf-8 -*-
"""test class"""
import os
import unittest

from plasoscaffolder.dal import sqlite_query_execution
from tests.test_helper import path_helper


class SQLiteQueryExecutionTest(unittest.TestCase):
  """test the SQLite Query execution test"""

  def setUp(self):
    database_path = path_helper.TestDatabasePath()
    file_path = os.path.join(database_path, 'twitter_ios.db')
    self.execute = sqlite_query_execution.SQLiteQueryExecution(file_path)
    self.execute.TryToConnect()

    file_path_types = os.path.join(database_path, 'test_database_types.db')
    self.execute_types = sqlite_query_execution.SQLiteQueryExecution(
        file_path_types)
    self.execute_types.TryToConnect()

    file_path_names = os.path.join(database_path, 'test_database_names.db')
    self.execute_names = sqlite_query_execution.SQLiteQueryExecution(
        file_path_names)
    self.execute_names.TryToConnect()

  def testTryToConnect(self):
    """try to connect without error"""
    database_path = path_helper.TestDatabasePath()
    file_path = os.path.join(database_path, 'twitter_ios.db')
    execute = sqlite_query_execution.SQLiteQueryExecution(file_path)
    connected = execute.TryToConnect()
    self.assertTrue(connected)

  def testTryToConnectWithError(self):
    """try to connect 2 times resulting in a error"""
    database_path = path_helper.TestDatabasePath()
    file_path = os.path.join(database_path, 'twitter_ios_error.db')
    execute = sqlite_query_execution.SQLiteQueryExecution(file_path)
    connected = execute.TryToConnect()
    self.assertFalse(connected)

  def testRollbackWorks(self):
    """testing if the rollback works"""
    query_select_all_users = 'SELECT * FROM Users'
    query_drop_table = 'DROP TABLE Users'
    result_users_before = self.execute.ExecuteQuery(query_select_all_users)
    result_drop_table = self.execute.ExecuteQuery(query_drop_table)
    result_users_after = self.execute.ExecuteQuery(query_select_all_users)

    self.assertEqual(len(result_users_before.data),
                     len(result_users_after.data))
    self.assertTrue(len(result_users_after.data) is 25)
    self.assertTrue(len(result_users_before.data) is 25)
    self.assertFalse(result_drop_table.has_error)
    self.assertIsNone(result_drop_table.error_message)

  def testMultipleTestAfterOneAnother(self):
    """test two querys after another to test the connection is still open"""
    query_simple = ('SELECT createdDate, updatedAt, screenName, '
                    'Name, profileImageUrl,'
                    'location, description, url, following, followersCount, '
                    'followingCount'
                    ' FROM Users ORDER BY createdDate')
    result_simple = self.execute.ExecuteQuery(query_simple)

    query_join = ('SELECT Statuses.date AS date, Statuses.text AS text,'
                  ' Statuses.userId AS user_id, Users.Name AS Name, '
                  'Statuses.retweetCount AS '
                  'retweetCount, Statuses.favoriteCount AS favoriteCount, '
                  'Statuses.favorited AS favorited, Statuses.updatedAt AS '
                  'updatedAt '
                  'FROM Statuses LEFT join Users ON Statuses.userId = Users.id '
                  'ORDER BY date')
    result_join = self.execute.ExecuteQuery(query_join)

    self.assertIsNone(result_join.error_message)
    self.assertIsNone(result_simple.error_message)
    self.assertFalse(result_simple.has_error)
    self.assertFalse(result_join.has_error)
    self.assertEqual(len(result_join.data), 67)
    self.assertEqual(len(result_simple.data), 25)

  def testQueryErrorNoSuchColumn(self):
    """test two querys after another to test the connection is still open"""
    query = 'SELECT createdDates FROM Users'
    result = self.execute.ExecuteQuery(query)
    expected_error = 'Error: no such column: createdDates'
    self.assertTrue(result.has_error)
    self.assertIsNone(result.data)
    self.assertEqual(str(result.error_message), expected_error)

  def testQueryErrorNoSuchTable(self):
    """test two querys after another to test the connection is still open"""
    query = 'SELECT createdDate FROM Userss'
    result = self.execute.ExecuteQuery(query)
    expected_error = 'Error: no such table: Userss'
    self.assertTrue(result.has_error)
    self.assertIsNone(result.data)
    self.assertEqual(str(result.error_message), expected_error)

  def testQueryWarning(self):
    """test two querys after another to test the connection is still open"""
    query = 'SELECT id from users;Select id from users'
    result = self.execute.ExecuteQuery(query)
    expected_error = 'Warning: You can only execute one statement at a time.'
    self.assertTrue(result.has_error)
    self.assertIsNone(result.data)
    self.assertEqual(str(result.error_message), expected_error)

  def testExecuteQueryDetailedSimple(self):
    """test the execution of a simple Query"""
    query = ('SELECT createdDate, updatedAt, screenName, Name, profileImageUrl,'
             'location, description, url, following, followersCount, '
             'followingCount'
             ' FROM Users ORDER BY createdDate')
    result = self.execute.ExecuteQueryDetailed(query)
    expected_data = self._ReadFromFileRelative('expected_simple_query_data')
    self.assertIsNone(result.error_message)
    self.assertFalse(result.has_error)
    self.assertEqual(expected_data, str(result.data))

    self.assertEqual(result.columns[0].sql_column, 'createdDate')
    self.assertEqual(result.columns[1].sql_column, 'updatedAt')
    self.assertEqual(result.columns[2].sql_column, 'screenName')
    self.assertEqual(result.columns[3].sql_column, 'name')
    self.assertEqual(result.columns[4].sql_column, 'profileImageUrl')
    self.assertEqual(result.columns[5].sql_column, 'location')
    self.assertEqual(result.columns[6].sql_column, 'description')
    self.assertEqual(result.columns[7].sql_column, 'url')
    self.assertEqual(result.columns[8].sql_column, 'following')
    self.assertEqual(result.columns[9].sql_column, 'followersCount')
    self.assertEqual(result.columns[10].sql_column, 'followingCount')
    # Commenting out tests as part of project #1, issue #17.
    #self.assertEqual(result.columns[0].GetColumnTypeAsName(), 'float')
    #self.assertEqual(result.columns[1].GetColumnTypeAsName(), 'float')
    #self.assertEqual(result.columns[2].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[3].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[4].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[5].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[6].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[7].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[8].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[9].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[10].GetColumnTypeAsName(), 'int')

  def testExecuteQueryDetailedWithOneDuplicateColumnNames(self):
    """test the execution of a simple Query with one duplicate column name"""
    query = ('SELECT t1.a, t1.b, t2.a from t1 join t2')
    result = self.execute_names.ExecuteQueryDetailed(query)
    expected_error_message = 'Please use an alias (AS) for those column ' \
                             'names: a'
    self.assertTrue(result.has_error)
    self.assertEqual(result.error_message, expected_error_message)

  def testExecuteQueryDetailedWithTwoDuplicateColumnNames(self):
    """test the execution of a simple Query with two duplicate column names"""
    query = ('SELECT t1.a, t1.b, t2.a, t2.b from t1 join t2')
    result = self.execute_names.ExecuteQueryDetailed(query)
    expected_error_message = 'Please use an alias (AS) for those column ' \
                             'names: a b'
    self.assertTrue(result.has_error)
    self.assertEqual(result.error_message, expected_error_message)

  def testExecuteQueryDetailedWithJoin(self):
    """test the execution of a more complex Query"""
    query = ('SELECT Statuses.date AS date, Statuses.text AS text,'
             ' Statuses.userId AS user_id, Users.Name AS Name, '
             'Statuses.retweetCount AS '
             'retweetCount, Statuses.favoriteCount AS favoriteCount, '
             'Statuses.favorited AS favorited, Statuses.updatedAt AS updatedAt '
             'FROM Statuses LEFT join Users ON Statuses.userId = Users.id '
             'ORDER BY date')
    result = self.execute.ExecuteQueryDetailed(query)
    expected_data = self._ReadFromFileRelative('expected_join_query_data')
    self.assertIsNone(result.error_message)
    self.assertFalse(result.has_error)
    self.assertEqual(expected_data, str(result.data))

    self.assertEqual(result.columns[0].sql_column, 'date')
    self.assertEqual(result.columns[1].sql_column, 'text')
    self.assertEqual(result.columns[2].sql_column, 'user_id')
    self.assertEqual(result.columns[3].sql_column, 'Name')
    self.assertEqual(result.columns[4].sql_column, 'retweetCount')
    self.assertEqual(result.columns[5].sql_column, 'favoriteCount')
    self.assertEqual(result.columns[6].sql_column, 'favorited')
    self.assertEqual(result.columns[7].sql_column, 'updatedAt')
    # Commenting out tests as part of project #1, issue #17.
    #self.assertEqual(result.columns[0].GetColumnTypeAsName(), 'float')
    #self.assertEqual(result.columns[1].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[2].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[3].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[4].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[5].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[6].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[7].GetColumnTypeAsName(), 'float')

  def testExecuteQueryDetailedWithSpecialCharacters(self):
    """test the execution of a more complex Query"""
    query = ('SELECT [AS].[id] as [AS], [AS].name as "name" from Users AS [AS]')

    result = self.execute.ExecuteQueryDetailed(query)
    expected_error_message = ('Warning: Don\'t use any characters beside '
                              'a-z A-Z 0-9 . ; , * = _')
    self.assertTrue(result.has_error)
    self.assertEqual(result.error_message, expected_error_message)
    self.assertEqual(result.error_message, expected_error_message)

  def testExecuteQueryDetailedWithAliasWithUnderscore(self):
    """test the execution of a more complex Query"""
    query = ('SELECT id as the_id, name as the_name from users')

    result = self.execute.ExecuteQueryDetailed(query)
    expected_data = self._ReadFromFileRelative('expected_id_name_data')
    self.assertIsNone(result.error_message)
    self.assertFalse(result.has_error)
    self.assertEqual(expected_data, str(result.data))

  def testExecuteQueryDetailedWithAliasWithUnderscore2(self):
    """test the execution of a more complex Query"""
    query = ('SELECT users.id as the_id, name as the_name from users')

    result = self.execute.ExecuteQueryDetailed(query)
    expected_data = self._ReadFromFileRelative('expected_id_name_data')
    self.assertIsNone(result.error_message)
    self.assertFalse(result.has_error)
    self.assertEqual(expected_data, str(result.data))

  def testExecuteQueryDetailedWithAliasWithUnderscore3(self):
    """test the execution of a more complex Query"""
    query = ('SELECT users.id as the_id, name as the_name '
             'from users join statuses')

    result = self.execute.ExecuteQueryDetailed(query)
    expected_data = self._ReadFromFileRelative('expected_id_name_join_data')
    self.assertIsNone(result.error_message)
    self.assertFalse(result.has_error)
    self.assertEqual(expected_data, str(result.data))

  def testExecuteQueryDetailedWithJoinAndAliasWithUnderscore(self):
    """test the execution of a more complex Query"""
    query = ('SELECT users.id as the_id, users.name as the_name '
             'from users join statuses')

    result = self.execute.ExecuteQueryDetailed(query)
    expected_data = self._ReadFromFileRelative('expected_id_name_join_data')
    self.assertIsNone(result.error_message)
    self.assertFalse(result.has_error)
    self.assertEqual(expected_data, str(result.data))

  def testExecuteQueryDetailedWithAliasForTable(self):
    """test the execution of a more complex Query"""
    query = ('SELECT x.id, x.name from users as x')
    result = self.execute.ExecuteQueryDetailed(query)
    expected_error_message = ('Warning: Don\'t use any alias for a table name')
    self.assertTrue(result.has_error)
    self.assertEqual(result.error_message, expected_error_message)

  def testExecuteQueryReadOnlyWithAliasForMultipleTable(self):
    """test the execution of a more complex Query"""
    query = ('SELECT x.id, x.name from users as x join statuses')
    result = self.execute.ExecuteQueryDetailed(query)
    expected_error_message = ('Warning: Don\'t use any alias for a table name')
    self.assertTrue(result.has_error)
    self.assertEqual(result.error_message, expected_error_message)

  def testExecuteQueryDetailedWithJoinAndAliasForTable(self):
    """test the execution of a more complex Query"""
    query = ('SELECT x.id as userid, x.name, y.id as statusid '
             'from users as x join statuses as y')
    result = self.execute.ExecuteQueryDetailed(query)
    expected_error_message = ('Warning: Don\'t use any alias for a table name')
    self.assertTrue(result.has_error)
    self.assertEqual(result.error_message, expected_error_message)

  def testExecuteQueryDetailedWithJoinAndNoTable(self):
    """test the execution of a more complex Query"""
    query = ('SELECT users.id, name from users join statuses')
    result = self.execute.ExecuteQueryDetailed(query)
    expected_data = self._ReadFromFileRelative('expected_id_name_join_data')
    self.assertIsNone(result.error_message)
    self.assertFalse(result.has_error)
    self.assertEqual(expected_data, str(result.data))

  def testExecuteReadOnlyQueryWithSelect(self):
    """test execute read only with a simple select query"""
    query = 'SELECT id from users where id==2220776716'
    result = self.execute.ExecuteReadOnlyQuery(query)
    expected = '[(2220776716,)]'
    self.assertFalse(result.has_error)
    self.assertEqual(str(result.data), expected)
    self.assertIsNone(result.error_message)
    self.assertEqual(result.columns[0].sql_column, 'id')
    # Commenting out tests as part of project #1, issue #17.
    #self.assertEqual(result.columns[0].GetColumnTypeAsName(), 'int')

  def testExecuteQueryDetailedSimpleNoData(self):
    """test the execution of a simple Query"""
    query = ('SELECT * From nodata')
    result = self.execute_types.ExecuteQueryDetailed(query)
    expected_data = '[]'
    self.assertIsNone(result.error_message)
    self.assertFalse(result.has_error)
    self.assertEqual(expected_data, str(result.data))

    self.assertEqual(result.columns[0].sql_column, 'intval')
    self.assertEqual(result.columns[1].sql_column, 'integerval')
    self.assertEqual(result.columns[2].sql_column, 'tinyintval')
    self.assertEqual(result.columns[3].sql_column, 'smallintval')
    self.assertEqual(result.columns[4].sql_column, 'mediuintval')
    self.assertEqual(result.columns[5].sql_column, 'bigintval')
    self.assertEqual(result.columns[6].sql_column, 'unsignedbigintval')
    self.assertEqual(result.columns[7].sql_column, 'int2val')
    self.assertEqual(result.columns[8].sql_column, 'int8val')
    self.assertEqual(result.columns[9].sql_column, 'characterval')
    self.assertEqual(result.columns[10].sql_column, 'varcharval')
    self.assertEqual(result.columns[11].sql_column, 'varyingcharacterval')
    self.assertEqual(result.columns[12].sql_column, 'ncharval')
    self.assertEqual(result.columns[13].sql_column, 'nativecharacterval')
    self.assertEqual(result.columns[14].sql_column, 'nvarcharval')
    self.assertEqual(result.columns[15].sql_column, 'textval')
    self.assertEqual(result.columns[16].sql_column, 'clobval')
    self.assertEqual(result.columns[17].sql_column, 'blobval')
    self.assertEqual(result.columns[18].sql_column, 'realval')
    self.assertEqual(result.columns[19].sql_column, 'doubleval')
    self.assertEqual(result.columns[20].sql_column, 'doubleprecisionval')
    self.assertEqual(result.columns[21].sql_column, 'floatval')
    self.assertEqual(result.columns[22].sql_column, 'numericval')
    self.assertEqual(result.columns[23].sql_column, 'decimalval')
    self.assertEqual(result.columns[24].sql_column, 'booleanval')
    self.assertEqual(result.columns[25].sql_column, 'dateval')
    self.assertEqual(result.columns[26].sql_column, 'datetimeval')
    # Commenting out tests as part of project #1, issue #17.
    #self.assertEqual(result.columns[0].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[1].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[2].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[3].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[4].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[5].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[6].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[7].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[8].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[9].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[10].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[12].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[13].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[14].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[15].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[16].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[17].GetColumnTypeAsName(), 'bytes')
    #self.assertEqual(result.columns[18].GetColumnTypeAsName(), 'float')
    #self.assertEqual(result.columns[19].GetColumnTypeAsName(), 'float')
    #self.assertEqual(result.columns[20].GetColumnTypeAsName(), 'float')
    #self.assertEqual(result.columns[21].GetColumnTypeAsName(), 'float')
    #self.assertEqual(result.columns[22].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[23].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[24].GetColumnTypeAsName(), 'bool')
    #self.assertEqual(result.columns[25].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[26].GetColumnTypeAsName(), 'int')

  def testExecuteQueryDetailedJoinNoData(self):
    """test the execution of a join Query with no data"""
    query = ('SELECT t1.a as a, t2.a as a2, t2.c, t1.b, t2.b as b2 '
             'from t1 join t2')
    result = self.execute_names.ExecuteQueryDetailed(query)
    expected_data = '[]'
    self.assertIsNone(result.error_message)
    self.assertFalse(result.has_error)
    self.assertEqual(expected_data, str(result.data))

    self.assertEqual(result.columns[0].sql_column, 'a')
    self.assertEqual(result.columns[1].sql_column, 'a2')
    self.assertEqual(result.columns[2].sql_column, 'c')
    self.assertEqual(result.columns[3].sql_column, 'b')
    self.assertEqual(result.columns[4].sql_column, 'b2')
    # Commenting out tests as part of project #1, issue #17.
    #self.assertEqual(result.columns[0].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[1].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[2].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[3].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[4].GetColumnTypeAsName(), 'str')

  def testExecuteQueryDetailedJoinNoDataNoSpace(self):
    """test the execution of a join Query with no data"""
    query = ('SELECT t1.a as a,t2.a as a2,t2.c, t1.b,t2.b as b2 '
             'from t1 join t2')
    result = self.execute_names.ExecuteQueryDetailed(query)
    expected_data = '[]'
    self.assertIsNone(result.error_message)
    self.assertFalse(result.has_error)
    self.assertEqual(expected_data, str(result.data))

    self.assertEqual(result.columns[0].sql_column, 'a')
    self.assertEqual(result.columns[1].sql_column, 'a2')
    self.assertEqual(result.columns[2].sql_column, 'c')
    self.assertEqual(result.columns[3].sql_column, 'b')
    self.assertEqual(result.columns[4].sql_column, 'b2')
    # Commenting out tests as part of project #1, issue #17.
    #self.assertEqual(result.columns[0].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[1].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[2].GetColumnTypeAsName(), 'str')
    #self.assertEqual(result.columns[3].GetColumnTypeAsName(), 'int')
    #self.assertEqual(result.columns[4].GetColumnTypeAsName(), 'str')

  def testExecuteQuerySimple(self):
    """test the execution of a simple Query"""
    query = ('SELECT createdDate, updatedAt, screenName, Name, profileImageUrl,'
             'location, description, url, following, followersCount, '
             'followingCount'
             ' FROM Users ORDER BY createdDate')
    result = self.execute.ExecuteQuery(query)
    expected_data = self._ReadFromFileRelative('expected_simple_query_data')
    self.assertIsNone(result.error_message)
    self.assertFalse(result.has_error)
    self.assertEqual(expected_data, str(result.data))
    self.assertIsNone(result.columns)

  def testExecuteReadOnlyQueryWithErrorBecauseOfDrop(self):
    """test execute read only with a drop query"""
    query = 'DROP table users'
    result = self.execute.ExecuteReadOnlyQuery(query)
    expected_error = 'Query has to be a single SELECT query.'
    self.assertTrue(result.has_error)
    self.assertEqual(str(result.error_message), expected_error)
    self.assertIsNone(result.data)
    self.assertIsNone(result.columns)

  def testExecuteReadOnlyQueryWithErrorBecauseOfAlter(self):
    """test execute read only with a alter rename query"""
    query = 'Alter table users rename to users2'
    result = self.execute.ExecuteReadOnlyQuery(query)
    expected_error = 'Query has to be a single SELECT query.'
    self.assertTrue(result.has_error)
    self.assertEqual(str(result.error_message), expected_error)
    self.assertIsNone(result.data)
    self.assertIsNone(result.columns)

  def testExecuteReadOnlyQueryWithWarning(self):
    """test execute read only with two queries at the same time"""
    query = 'SELECT id from users;SELECT id from users;'
    result = self.execute.ExecuteReadOnlyQuery(query)
    expected_error = 'Warning: You can only execute one statement at a time.'
    self.assertTrue(result.has_error)
    self.assertEqual(str(result.error_message), expected_error)
    self.assertIsNone(result.data)
    self.assertIsNone(result.columns)

  def _ReadFromFileRelative(self, path: str):
    """Read from file with relative path

    Args:
      path (str): the relative file path

    Returns:
      str: content of the file"""
    current_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(current_dir, path)

    with open(abs_file_path, 'r', encoding='utf-8') as f:
      return f.read()


if __name__ == '__main__':
  unittest.main()
