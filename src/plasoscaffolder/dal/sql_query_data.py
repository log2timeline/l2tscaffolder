# -*- coding: utf-8 -*-
"""Data class for the SQL Query"""
from plasoscaffolder.model import sql_query_column_model


class SQLQueryData(object):
  """The Data to the executed query.

  Attributes:
    has_error (bool): if the query execution was erroneous
    data ([str]): the rows returned after execution
    error_message(str): the error message if the query was erroneous
    columns ([sql_query_column_model.SQLColumnModel]): the column names of
        the query
  """

  def __init__(self, has_error: bool=False, data: []=None,
               error_message: str=None,
               columns: [sql_query_column_model.SQLColumnModel]=None):
    self.has_error = has_error
    self.data = data
    self.error_message = error_message
    self.columns = columns
