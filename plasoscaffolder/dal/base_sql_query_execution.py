# -*- coding: utf-8 -*-
# disable warning because default value is not dangerous here
"""The SQLite Query validator."""
import abc

from plasoscaffolder.dal import sql_query_data


class BaseSQLQueryExecution(object):
  """Class representing the SQLite query validator."""

  @abc.abstractmethod
  def ExecuteQuery(self, query: str) -> sql_query_data.SQLQueryData:
    """Executes the SQL Query.

    Args:
      query (str): The SQL Query to execute on the SQLite database.

    Returns:
      sql_query_data.SQLQueryData: The data to the Query
    """

  @abc.abstractmethod
  def TryToConnect(self) -> bool:
    """Try to open the database File.

    Returns:
      bool: if the file can be opened and is a database file
    """

  @abc.abstractmethod
  def ExecuteReadOnlyQuery(self, query: str) -> sql_query_data.SQLQueryData:
    """Executes the SQL Query if it is read only, and valid to parse.

      Args:
        query (str): the SQL Query to execute on the SQLite database

      Returns:
        sql_query_data.SQLQueryData: the data to the Query
    """

  @abc.abstractmethod
  def ExecuteQueryDetailed(
      self, query: str) -> sql_query_data.SQLQueryData:
    """Executes the SQL Query and gets detailed information.

    Args:
      query (str): The SQL Query to execute on the SQLite database.

    Returns:
      sql_query_data.SQLQueryData: The data to the Query
    """
