# -*- coding: utf-8 -*-
"""The parser model class."""
from plasoscaffolder.model import base_data_model
from plasoscaffolder.model import sql_query_model


class ParserDataModel(base_data_model.BaseDataModel):
  """Class for the data for the parser template."""

  def __init__(self,
               plugin_name: str,
               queries: [sql_query_model.SQLQueryModel],
               required_tables: [str],
               database_name: str):
    """Initialises the parser data model.

    Args:
      plugin_name (str): the name of the plugin
      queries ([sql_query_model.SQLQueryModel]): the queries
      required_tables ([str]): the tables that are required
      database_name (str): the name of the database
    """
    super().__init__(plugin_name)
    self.queries = queries
    self.required_tables = required_tables
    self.database_name = database_name
