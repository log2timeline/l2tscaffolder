# -*- coding: utf-8 -*-
"""Base class for SQLite plugin helper"""
import abc

from plasoscaffolder.bll.services import base_sqlite_plugin_path_helper
from plasoscaffolder.dal import base_sql_query_execution
from plasoscaffolder.dal import sql_query_data
from plasoscaffolder.model import sql_query_column_model
from plasoscaffolder.model import sql_query_column_model_data
from plasoscaffolder.model import sql_query_column_model_timestamp
from plasoscaffolder.model import sql_query_model


class BaseSQLitePluginHelper(object):
  """Class representing the base class for the SQLite plugin helper."""
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def PluginExists(
      self,
      path: str,
      plugin_name: str,
      database_suffix: str,
      path_helper: base_sqlite_plugin_path_helper.BaseSQLitePluginPathHelper
  ) -> bool:
    """Checks if the plugin already exists.

    Args:
      database_suffix: the suffix of the database file
      path (str): the path of the plaso source
      plugin_name (str): the name of the plugin
      path_helper (base_sqlite_plugin_path_helper.BaseSQLitePluginPathHelper):
          the SQLite plugin helper

    Returns:
      bool: True if the plugin already exists. False if it does not.
    """

  @abc.abstractmethod
  def FileExists(self, path: str) -> bool:
    """Checks if the file exists.

    Args:
       path (str): the file path
    """

  @abc.abstractmethod
  def FolderExists(self, path: str) -> bool:
    """Checks if folder exists.

    Args:
      path (str): the folder path
    """

  @abc.abstractmethod
  def IsValidPluginName(self, plugin_name: str) -> bool:
    """Validates the plugin Name.

    Args:
      plugin_name (str): the plugin Name

    Returns:
      bool: true if the plugin Name is valid
    """

  @abc.abstractmethod
  def IsValidRowName(self, row_name: str) -> bool:
    """Validates the row name.

    Args:
      row_name (str): the row name

    Returns:
      bool: true if the row name is valid
    """

  @abc.abstractmethod
  def IsValidCommaSeparatedString(self, text: str) -> bool:
    """Validates a comma separated string

    Args:
      text (str): the string to validate

    Returns:
      bool: true if the text is valide
    """

  @abc.abstractmethod
  def RunSQLQuery(
      self, query: str,
      executor: base_sql_query_execution.BaseSQLQueryExecution
  ) -> sql_query_data.SQLQueryData:
    """ Validates the sql query

    Args:
      executor (base_sql_query_execution.SQLiteQueryExecution): to validate the
        SQL queries provided by the user
      query (str): the SQL query

    Returns:
      sql_query_data.SQLQueryData: data returned by executing the
        query
    """

  @abc.abstractmethod
  def GetDistinctColumnsFromSQLQueryData(
      self,
      queries: [sql_query_model.SQLQueryModel]) -> [str]:
    """
    Get a distinct list of all attributes from multiple queries

    Args:
      queries ([sql_query_model.SQLQueryModel]): an array of multiple
        sql query data objects

    Returns:
      list[str]: all distinct attributes used in the query
    """

  @abc.abstractmethod
  def GetAssumedTimestamps(self, columns: [sql_query_column_model]) -> [str]:
    """Gets all columns assumed that they are timestamps

    Args:
      columns ([sql_query_column_model]): the columns from the query

    Returns:
      [str]: the names from the columns assumed they could be a timestamp
    """

  @abc.abstractmethod
  def GetColumnsAndTimestampColumn(
      self, columns: [sql_query_column_model.SQLColumnModel],
      timestamps: [str], data: [str]
  ) -> (
      [sql_query_column_model_data.SQLColumnModelData],
      [sql_query_column_model_timestamp.SQLColumnModelTimestamp]):
    """Splits the column list into a list of simple columns and a list for
    timestamp event columns and adds the data to the simple columns

    Args:
      columns ([sql_query_column_model_data.SQLColumnModelData]): the columns
          from the SQL query
      timestamps ([str]): the timestamp events
      data ([str]): the data from the cursor

    Returns:
      ([sql_query_column_model_data.SQLColumnModelData],
          [sql_query_column_model_timestamp.SQLColumnModelTimestamp): a tuple
          of columns, the first are the normal columns, the second are the
          timestamp events
    """
