# -*- coding: utf-8 -*-
# this default value is just for testing in a fake.
# pylint: disable=dangerous-default-value
"""Fake class for the explain query plan."""

from plasoscaffolder.dal import base_explain_query_plan


class FakeExplainQueryPlan(base_explain_query_plan.BaseExplainQueryPlan):
  """Fake class representing the explain query plan."""

  def __init__(self, is_read_only: bool=True, locked_tables: []=[]):
    """Initializes the explain query plan.

    Args:
      is_read_only: what the method IsReadOnly should return
      locked_tables: what the method GetLockedTables should return
    """
    super().__init__()
    self.is_read_only = is_read_only
    self.locked_tables = locked_tables

  def IsReadOnly(self, query: str) -> bool:
    """Determines if the query is read only.

    Args:
      query (str): the sql query to determine if it is read only

    Returns:
      bool: true if it is read only, false if it is not
    """
    return self.is_read_only

  def GetLockedTables(self, query: str) -> [str]:
    """Determines the table that were locked during the SQL query.

    Args:
      query (str): the sql query to get the locked tables from

    Returns:
      [str]: the list of tables
    """
    return self.locked_tables
