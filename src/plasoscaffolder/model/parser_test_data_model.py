# -*- coding: utf-8 -*-
"""The parser test model class."""
from plasoscaffolder.model import base_data_model
from plasoscaffolder.model import sql_query_model


class ParserTestDataModel(base_data_model.BaseDataModel):
  """Class for the data for the parser test template."""

  def __init__(self,
               plugin_name: str,
               queries: [sql_query_model.SQLQueryModel],
               database_name: str):
    """Initialises the parser test data model.

    Args:
      plugin_name (str): the name of the plugin
      queries ([sql_query_model.SQLQueryModel]): the queries
      database_name (str): the name of the database
    """
    super().__init__(plugin_name)
    self.queries = queries
    self.database_name = database_name
