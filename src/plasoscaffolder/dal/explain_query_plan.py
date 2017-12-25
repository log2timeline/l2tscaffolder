# -*- coding: utf-8 -*-
# pylint: disable=no-member
# pylint does not recognize connect and close as member
"""Class for the explain query plan."""

from plasoscaffolder.dal import base_explain_query_plan
from plasoscaffolder.dal import base_sql_query_execution


class ExplainQueryPlan(base_explain_query_plan.BaseExplainQueryPlan):
  """Class representing the explain query plan."""

  def __init__(self,
               sql_execution: base_sql_query_execution.BaseSQLQueryExecution):

    """Initializes the explain query plan.

    Args:
      sql_execution (base_sql_query_execution.BaseSQLQueryExecution): the
          helper to execute a query
    """
    super().__init__()
    self._sql_execution = sql_execution

  def IsReadOnly(self, query: str) -> bool:
    """Determines if the query is read only.

    Args:
      query (str): the sql query to determine if it is read only

    Returns:
      bool: true if it is read only, false if it is not
    """
    explain_query = 'EXPLAIN {0}'.format(query)
    explain_result = self._sql_execution.ExecuteQuery(explain_query)
    if explain_result.has_error:
      return False
    opcodes = [explain_row[1] for explain_row in explain_result.data]
    has_write = 'OpenWrite' in opcodes
    self.GetLockedTables(query)
    return not has_write

  def GetLockedTables(self, query: str) -> [str]:
    """Determines the table that were locked during the SQL query.

    Args:
      query (str): the sql query to get the locked tables from

    Returns:
      [str]: the list of tables
    """
    explain_query = 'EXPLAIN {0}'.format(query)
    explain_result = self._sql_execution.ExecuteQuery(explain_query)
    if explain_result.has_error or explain_result.data is None:
      return []
    tables = [explain_row[5] for explain_row in explain_result.data if
              explain_row[1] == 'TableLock']
    return tables
