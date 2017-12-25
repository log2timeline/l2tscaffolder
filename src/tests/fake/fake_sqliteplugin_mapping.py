# -*- coding: utf-8 -*-
"""fake formatter mapper"""
from plasoscaffolder.bll.mappings import base_mapping_helper
from plasoscaffolder.bll.mappings import base_sqliteplugin_mapping
from plasoscaffolder.model import base_data_model


class FakeSQLitePluginMapper(base_sqliteplugin_mapping.BaseSQLitePluginMapper):
  """class representing the fake parser mapper"""

  def __init__(self, mapping_helper: base_mapping_helper.BaseMappingHelper):
    pass

  def GetRenderedTemplate(
      self,
      data: base_data_model.BaseDataModel) -> str:
    return data.plugin_name
