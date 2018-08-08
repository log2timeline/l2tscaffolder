# -*- coding: utf-8 -*-
"""Class representing the mapper for the parser test file."""
from plasoscaffolder.bll.mappings import base_mapping_helper
from plasoscaffolder.bll.mappings import base_sqliteplugin_mapping
from plasoscaffolder.model import parser_test_data_model, sql_query_model


class ParserTestMapper(base_sqliteplugin_mapping.BaseSQLitePluginMapper):
  """Class representing the parser mapper."""

  _PARSER_TEST_TEMPLATE = 'parser_test_template.jinja2'

  def __init__(self,
               mapping_helper: base_mapping_helper.BaseMappingHelper):
    """Initializing the mapper class.

    Args:
      mapping_helper (base_mapping_helper.BaseMappingHelper): the helper class
          for the mapping
    """
    super().__init__()
    self._helper = mapping_helper

  def GetRenderedTemplate(
      self,
      parser_test_data: parser_test_data_model.ParserTestDataModel) -> str:
    """Retrieves the parser test.

    Args:
      parser_test_data (parser_test_data_model.ParserTestDataModel): the data
         for the parser test

    Returns:
      str: the rendered template
    """
    class_name = self._helper.GenerateClassName(parser_test_data.plugin_name)
    context = {'plugin_name': parser_test_data.plugin_name,
               'class_name': class_name,
               'queries': parser_test_data.queries,
               'database_name': parser_test_data.database_name,
               'count_events': self.GetAmountEvents(parser_test_data.queries)}
    rendered = self._helper.RenderTemplate(self._PARSER_TEST_TEMPLATE, context)
    return rendered

  def GetAmountEvents(self, queries: [sql_query_model.SQLQueryModel]) -> int:
    """Calculates the amount of events from the queries.

    Args:
      queries ([sql_query_model.SQLQueryModel]): the queries

    Returns:
      int: the amount of events
    """
    return sum([query.amount_events * len(query.timestamp_columns) for query in
                queries])
