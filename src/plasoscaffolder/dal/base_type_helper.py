# -*- coding: utf-8 -*-
"""Base SQLite Type Helper."""
import abc

from plasoscaffolder.model import sql_query_column_model


class BaseTypeHelper(object):
  """Base class representing the type helper for SQLite."""

  @abc.abstractmethod
  def GetDuplicateColumnNames(
      self, columns: sql_query_column_model.SQLColumnModel) -> [str]:
    """Find out if the query has duplicate column names and if a alias is
        needed.

    Args:
      columns (sql_query_column_model.SQLColumnModel): all columns parsed
          from the cursor
    Returns:
      [str]: a list of all the duplicate column names, if its empty it means it
          is a distinct list of columns
    """

  @abc.abstractmethod
  def GetColumnInformationFromDescription(
      self, description: []) -> [sql_query_column_model.SQLColumnModel]:
    """Getting Information for the column out of the cursor.

    Args:
      description: the description of the cursor

    Returns:
      [sql_query_column_model.SQLColumnModel]: a list with all the column
          names, the types are None
    """

  @abc.abstractmethod
  def AddMissingTypesFromSchema(
      self, columns: [sql_query_column_model.SQLColumnModel], query: str,
  ) -> [sql_query_column_model.SQLColumnModel]:
    """Getting Information for the column out of the cursor.

    Args:
      columns ([sql_query_column_model.SQLColumnModel]): the columns with all
          the column names
      query: the query

    Returns:
      [sql_query_column_model.SQLColumnModel]: a list with all the columns
    """
