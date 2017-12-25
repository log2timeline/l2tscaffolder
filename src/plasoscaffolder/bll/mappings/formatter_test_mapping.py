# -*- coding: utf-8 -*-
"""Class representing mapper for formatter test file."""
from plasoscaffolder.bll.mappings import base_mapping_helper
from plasoscaffolder.bll.mappings import base_sqliteplugin_mapping
from plasoscaffolder.model import formatter_test_data_model


class FormatterTestMapper(base_sqliteplugin_mapping.BaseSQLitePluginMapper):
  """Class representing the formatter test mapper."""

  _FORMATTER_TEST_TEMPLATE = 'formatter_test_template.jinja2'

  def __init__(self, mapping_helper: base_mapping_helper.BaseMappingHelper):
    """Initializing the init mapper class.

    Args:
      mapping_helper (base_mapping_helper.BaseMappingHelper): the helper class
          for the mapping
    """
    super().__init__()
    self._helper = mapping_helper

  def GetRenderedTemplate(
      self,
      formatter_test_data: formatter_test_data_model.FormatterTestDataModel
  ) -> str:
    """Retrieves the formatter test.

    Args:
      formatter_test_data (formatter_test_data_model.FormatterTestDataModel):
          the data for the formatter test

    Returns:
      str: the rendered template
    """
    class_name = self._helper.GenerateClassName(formatter_test_data.plugin_name)
    context = {'plugin_name': formatter_test_data.plugin_name,
               'class_name': class_name,
               'queries': formatter_test_data.queries}
    rendered = self._helper.RenderTemplate(
        self._FORMATTER_TEST_TEMPLATE, context)
    return rendered
