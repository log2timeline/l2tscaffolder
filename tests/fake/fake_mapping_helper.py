# -*- coding: utf-8 -*-
"""fake for __helper methods for mapping"""
from plasoscaffolder.bll.mappings import base_mapping_helper


class FakeMappingHelper(base_mapping_helper.BaseMappingHelper):
  """Fake for the mapping helper."""

  def __init__(self, template_path: str):
    self.template_path = template_path

  def RenderTemplate(self, template_filename: str, context: dict) -> str:
    return "fake string " + template_filename

  def GenerateClassName(self, plugin_name: str) -> str:
    return "fake class __name " + plugin_name
