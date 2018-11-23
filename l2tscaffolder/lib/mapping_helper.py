# -*- coding: utf-8 -*-
"""Helper methods for mapping."""
import os
import jinja2

from l2tscaffolder.lib import code_formatter


class MappingHelper:
  """Mapping helper for scaffolders."""

  _DEFAULT_PATH_FORMATTER = '.style.yapf'
  _DEFAULT_PATH_TEMPLATE = 'templates'

  def __init__(self, template_path: str='', formatter_path: str=''):
    """Initializes the mapping helper class.

    Args:
        template_path (Optional[str]):  file path to the templates diretory,
            relative to the path to the tool. If none provided will use the
            default path.
        formatter_path (Optional[str]):  file path of the formatter, relative
            to the path to the tool. If none provided will use the default
            path.
    """
    super(MappingHelper, self).__init__()
    # TODO: Improve this, this is flaky.
    self._tool_path = os.path.dirname(
        os.path.dirname(os.path.realpath(__file__)))

    if not template_path:
      template_path = self._DEFAULT_PATH_TEMPLATE
    # TODO: Check if the project has a YAPF config file and use that instead of
    # falling back to a default one.
    if not formatter_path:
      formatter_path = self._DEFAULT_PATH_FORMATTER

    full_template_path = os.path.join(self._tool_path, template_path)
    self._template_path = full_template_path
    template_loader = jinja2.FileSystemLoader(self._template_path)
    # TODO: Check if autoescape can be set to True due to potential XSS issues.
    self._template_environment = jinja2.Environment(
        autoescape=False, loader=template_loader, trim_blocks=False)

    full_formatter_path = os.path.join(self._tool_path, formatter_path)
    self.formatter = code_formatter.CodeFormatter(full_formatter_path)

  def _RemoveWhitespaceAtEndOfLine(self, template: str) -> str:
    """Removes blanks at the end of lines.

    This is for those parts that are ignored with yapf.

    Args:
      template (str): template to remove end-of-line whitespace from.

    Returns:
      str: template without end-of-line whitespace.
    """
    while template.find('  \n') != -1:
      template = template.replace('  \n', '\n')
    return template

  def _RemoveEscapeError(self, template: str) -> str:
    """Removes the escape error.

    Because jinja template variable is first escaped and then word wrapped,
    the escaped backslash can be split and can result in an EOL.
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

    return template.replace(to_be_replaced, to_be_replaced_with)

  def _RemoveYapfComment(self, template: str) -> str:
    """Removes the yapf comment line.

    The line as well as the new line will be removed.
    The yapf comment has to be at the end of the line, or on its own line.

    Args:
      template (str): template to remove yapf comments from.

    Returns:
      str: template with yapf comments removed.
    """
    return template.replace('# yapf: disable\n', '').replace(
        '# yapf: enable\n', '')

  def GenerateClassName(self, scaffolder_name: str) -> str:
    """Generates a class name from the scaffolder name for file generation.

    Args:
      scaffolder_name (str): name of the scaffolder

    Returns:
      str: name of the class
    """
    return scaffolder_name.replace('_', ' ').title().replace(' ', '')

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
    formatted = self._RemoveWhitespaceAtEndOfLine(formatted)

    return formatted
