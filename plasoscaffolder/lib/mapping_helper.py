# -*- coding: utf-8 -*-
"""Helper methods for mapping."""
import abc
import os
import jinja2

from plasoscaffolder.lib import code_formatter


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


class ParserMapper(BaseMappingHelper):
  """Mapping Helper class for parsers."""

  def __init__(self):
    """Initializing the mapping helper class."""
    super(ParserMapper, self).__init__()
    self._template_path = ''
    self._template_environment = None
    self.formatter = None

  def _RemoveBlanksAtEndOfLine(self, template: str) -> str:
    """Removes blanks at the end of lines.

    This is for those parts that are ignored with yapf.

    Args:
      template (str): the template to remove the blanks at the end of lines

    Returns:
      str: the template without blanks on the line endings
    """
    while template.find('  \n') != -1:
      template = template.replace('  \n', '\n')
    return template

  def _RemoveEscapeError(self, template: str) -> str:
    """Remove the escape error.

    Because jinja template variable is first escaped and then word wrapped,
    the escaped backslash can be split and can result in an eol.
    The escaped backslash will be placed on the next line.
    This is a workaround and can be removed if yapf supports unicode string
    formatting and it is also changed in the jinja2 template, and only works
    with 8 spaces.

    Args:
      template (str): the resulting template as a python file string

    Returns:
      str: the template without escape (eol) errors
    """

    to_be_replaced = '\\\'\n        u\'\\'
    to_be_replaced_with = '\'\n        u\'\\\\'

    template = template.replace(to_be_replaced, to_be_replaced_with)
    return template

  def _RemoveYapfComment(self, template: str) -> str:
    """Remove the yapf comment line.

    The Line as well as the new line will be removed.
    The yapf Comment has to be at the end of the line. Or on its own line.

    Args:
      template (str): the resulting template as a python file string

    Returns:
      str: the template without yapf comment lines
    """
    return template.replace('# yapf: disable\n', '').replace(
        '# yapf: enable\n', '')

  def GenerateClassName(self, plugin_name: str) -> str:
    """Generates the class name from the plugin name.

    Args:
      plugin_name (str): the name of the plugin

    Returns:
      str: the name of the class
    """
    return plugin_name.replace('_', ' ').title().replace(' ', '')

  def RenderTemplate(self, template_filename: str, context: dict) -> str:
    """Renders the template with the context to return a string.

    Args:
      template_filename (str): the name of the template
      context (dict): the context of the template as a dictionary

    Returns:
      str: the rendered template as a string
    """
    template = self._template_environment.get_template(
        template_filename).render(context)
    template = self._RemoveEscapeError(template)

    formatted = self.formatter.Format(template)[0]
    formatted = self._RemoveYapfComment(formatted)
    formatted = self._RemoveBlanksAtEndOfLine(formatted)

    return formatted

  def SetDefaultPaths(self):
    """Sets both template and formatter path to a default path."""
    # TODO: Improve this, this is flaky.
    tool_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    template_path = os.path.join(tool_path, 'templates')
    self.SetTemplatePath(template_path)

    formatter_path = os.path.join(tool_path, '.style.yapf')
    self.SetFormatterPath(formatter_path)

  def SetTemplatePath(self, template_path: str):
    """Set the template path for the parser mapper."""
    self._template_path = template_path
    template_loader = jinja2.FileSystemLoader(self._template_path)
    # TODO: Check if autoescape can be set to True due to potential XSS issues.
    self._template_environment = jinja2.Environment(
        autoescape=False, loader=template_loader, trim_blocks=False)

  def SetFormatterPath(self, formatter_path: str):
    """Set the path to the formatter."""
    self.formatter = code_formatter.CodeFormatter(formatter_path)
