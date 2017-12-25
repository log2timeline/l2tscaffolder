# -*- coding: utf-8 -*-
"""The Base data model class."""


class BaseDataModel(object):
  """Class for the data for the formatter template."""

  def __init__(self,
               plugin_name: str):
    """Initialises the base data model.

    Args:
      plugin_name (str): the name of the plugin
    """
    super().__init__()
    self.plugin_name = plugin_name
