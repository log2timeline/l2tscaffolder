# -*- coding: utf-8 -*-
# pylint: disable=no-member
# pylint does not recognize connect and close as member
"""SQLite Query Execution"""
import re
import sqlite3

from plasoscaffolder.dal import base_sql_query_execution
from plasoscaffolder.dal import explain_query_plan
from plasoscaffolder.dal import sql_query_data
from plasoscaffolder.dal import sqlite_database_information
from plasoscaffolder.dal import sqlite_type_helper


class SQLiteQueryExecution(base_sql_query_execution.BaseSQLQueryExecution):
  """Class representing the SQLite Query validator."""

  def __init__(self, database_path: str):
    """Initializes the SQL Query Validator.

    Args:
      database_path (str): the path to the SQLite database schema
    """
    super().__init__()
    self._database_path = database_path
    self._connection = None
    self._explain = None
    self._type_helper = None

  def TryToConnect(self) -> bool:
    """Try to open the database File.

    Returns:
      bool: if the file can be opened and is a database file
    """
    try:
      self._connection = sqlite3.connect(
          self._database_path)
      self._connection.isolation_level = None  # no autocommit mode
      self._explain = explain_query_plan.ExplainQueryPlan(self)
      # this query failes if is not a database or locked or anything went wrong
      self._connection.execute('PRAGMA schema_version')

      database_information = (
          sqlite_database_information.SQLiteDatabaseInformation(self))
      self._type_helper = sqlite_type_helper.SQLiteTypeHelper(
          self, self._explain, database_information)
    except sqlite3.Error:
      return False

    return True

  def ExecuteQuery(self, query: str) -> sql_query_data.SQLQueryData:
    """Executes the SQL Query.

    Args:
      query (str): The SQL Query to execute on the SQLite database.

    Returns:
      sql_query_data.SQLQueryData: The data to the Query
    """
    return self._ExecuteQuery(query, False)

  def ExecuteQueryDetailed(
      self, query: str) -> sql_query_data.SQLQueryData:
    """Executes the SQL Query and gets detailed information.

    Args:
      query (str): The SQL Query to execute on the SQLite database.

    Returns:
      sql_query_data.SQLQueryData: The data to the Query
    """
    query_data = sql_query_data.SQLQueryData(
        data=None, has_error=True, columns=None)
    if not re.fullmatch('[A-Za-z,.;*=_0-9 ]*', query):
      query_data.error_message = ('Warning: Don\'t use any characters beside'
                                  ' a-z A-Z 0-9 . ; , * = _')
      return query_data

    if query.lower()[query.lower().find(' from '):].find(' as ') != -1:
      query_data.error_message = ('Warning: '
                                  'Don\'t use any alias for a table name')
      return query_data

    data_from_executed_query = self._ExecuteQuery(query, True)
    if not data_from_executed_query.has_error:
      duplicate_names = self._type_helper.GetDuplicateColumnNames(
          data_from_executed_query.columns)
      if duplicate_names:
        duplicate_names_as_string = ' '.join(duplicate_names)
        data_from_executed_query.has_error = True
        data_from_executed_query.error_message = (
            'Please use an alias (AS) for '
            'those column names: {0}'.format(duplicate_names_as_string))
      if not data_from_executed_query.has_error:

        data_from_executed_query.columns = (
            self._type_helper.AddMissingTypesFromSchema(
                data_from_executed_query.columns, query))

    return data_from_executed_query

  def _ExecuteQuery(
      self, query: str, detailed: bool=True) -> sql_query_data.SQLQueryData:
    """Executes the SQL Query.

    Args:
      query (str): The SQL Query to execute on the SQLite database.
      detailed (bool): True if additional information about the query is needed

    Returns:
      sql_query_data.SQLQueryData: The data to the Query
    """
    query_data = sql_query_data.SQLQueryData()
    try:
      with self._connection:
        self._connection.execute('BEGIN')
        cursor = self._connection.execute(query)
        query_data.data = cursor.fetchall()
        if detailed:
          query_data.columns = (
              self._type_helper.GetColumnInformationFromDescription(
                  cursor.description))
        self._connection.execute('ROLLBACK')
    except sqlite3.Error as error:
      query_data.error_message = 'Error: {0}'.format(str(error))
      query_data.has_error = True
    except sqlite3.Warning as warning:
      query_data.error_message = 'Warning: {0}'.format(str(warning))
      query_data.has_error = True

    return query_data

  def ExecuteReadOnlyQuery(self, query: str) -> sql_query_data.SQLQueryData:
    """Executes the SQL Query if it is read only, and valid to parse.

      Args:
        query (str): the SQL Query to execute on the SQLite database

      Returns:
        sql_query_data.SQLQueryData: the data to the Query
    """
    query_data = self.ExecuteQueryDetailed(query)
    if not query_data.has_error:
      if not self._explain.IsReadOnly(query):
        query_data.data = None
        query_data.has_error = True
        query_data.error_message = 'Query has to be a single SELECT query.'
        query_data.columns = None
    return query_data
