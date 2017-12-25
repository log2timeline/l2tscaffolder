# -*- coding: utf-8 -*-
"""Helper methods for mapping."""

import jinja2

from plasoscaffolder.bll.mappings import base_mapping_helper
from plasoscaffolder.common import code_formatter


class MappingHelper(base_mapping_helper.BaseMappingHelper):
  """Mapping Helper class."""

  def __init__(self, template_path: str, yapf_path: str):
    """Initializing the mapping helper class.

    Args:
      template_path (str): the path to the template directory
      yapf_path (str): the path to the yapf style file
    """
    super().__init__()
    template_loader = jinja2.FileSystemLoader(template_path)
    self._template_environment = jinja2.Environment(
        autoescape=False, loader=template_loader, trim_blocks=False)
    self.formatter = code_formatter.CodeFormatter(yapf_path)

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

  def GenerateClassName(self, plugin_name: str) -> str:
    """Generates the class name from the plugin name.

    Args:
      plugin_name (str): the name of the plugin

    Returns:
      str: the name of the class
    """
    return plugin_name.replace('_', ' ').title().replace(' ', '')

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
    return template.replace('# yapf: disable\n', '').replace('# yapf: enable\n',
                                                             '')

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
