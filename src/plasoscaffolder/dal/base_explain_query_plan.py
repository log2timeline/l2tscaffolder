# -*- coding: utf-8 -*-
# pylint: disable=no-member
# pylint does not recognize connect and close as member
"""Base class for the explain query plan."""
import abc


class BaseExplainQueryPlan(object):
  """Base class representing the explain query plan."""

  @abc.abstractmethod
  def IsReadOnly(self, query: str) -> bool:
    """Determines if the query is read only.

    Args:
      query (str): the sql query to determine if it is read only

    Returns:
      bool: true if it is read only, false if it is not
    """

  @abc.abstractmethod
  def GetLockedTables(self, query: str) -> [str]:
    """Determines the table that were locked during the SQL query.

    Args:
      query (str): the SQL query to get the locked tables from

    Returns:
      [str]: the list of tables
    """
