# -*- coding: utf-8 -*-
"""The SQL query model class."""
from plasoscaffolder.model import sql_query_column_model_data
from plasoscaffolder.model import sql_query_column_model_timestamp


class SQLQueryModel(object):
  """A SQL query model."""

  def __init__(
      self, query: str, name: str,
      columns: [sql_query_column_model_data.SQLColumnModelData],
      timestamp_columns: [
          sql_query_column_model_timestamp.SQLColumnModelTimestamp],
      needs_customizing: bool,
      amount_events: int
  ):
    """ initializes the SQL query model.

    Args:
      columns ([sql_query_column_model_data.SQLColumnModelData]): list of
          columns for the Query
      timestamp_columns ([
          sql_query_column_model_timestamp.SQLColumnModelTimestamp]): list of
          columns which are timestamp events
      name (str): The name of the Query.
      query (str): The SQL query.
      needs_customizing (bool): if the event for the query needs customizing
      amount_events (int): amount of events as result of the query
    """
    super().__init__()
    self.name = name
    self.query = query
    self.columns = columns
    self.needs_customizing = needs_customizing
    self.timestamp_columns = timestamp_columns
    self.amount_events = amount_events
