# -*- coding: utf-8 -*-
"""Helper methods for mapping."""
import abc


class BaseMappingHelper(object):
  """Base Mapping Helper base class."""
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def RenderTemplate(self, template_filename: str, context: dict) -> str:
    """Renders the template with the context to return a string.

    Args:
      template_filename (str): the name of the template
      context (dict): the context of the template as a dictionary

    Returns:
      str: the rendered template as a string
    """

  @abc.abstractmethod
  def GenerateClassName(self, plugin_name: str) -> str:
    """Generates the class name from the plugin name.

    Args:
      plugin_name (str): the name of the plugin

    Returns:
      str: the name of the class
    """
