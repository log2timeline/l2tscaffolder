# -*- coding: utf-8 -*-
"""The scaffolder interface classes."""
import abc
import collections

from typing import Dict
from typing import Iterator
from typing import List
from typing import Tuple

from plasoscaffolder.lib import definitions
from plasoscaffolder.lib import errors


Question = collections.namedtuple(
    'Question', ['attribute', 'prompt', 'help', 'type'])


class Scaffolder:
  """The scaffolder interface."""

  # The name of the component/parser/submodule this scaffolder generates.
  NAME = 'base_parser'

  # One liner describing what the scaffolder generates.
  DESCRIPTION = ''

  # Define which project this particular scaffolder belongs to.
  PROJECT = definitions.DEFINITION_PLASO

  # Questions, a list that contains all the needed questions that the
  # user should be prompted about before the plugin or parser is created.
  # Each element in the list should be of the named tuple question.
  QUESTIONS = []

  def __init__(self):
    """Initializes the scaffolder."""
    super(Scaffolder, self).__init__()
    self._output_name = ''

  def GetJinjaContext(self) -> Dict[str, object]:
    """Returns a dict that can be used as a context for Jinja2 templates."""
    return {}

  def GetQuestions(self) -> List[Question]:
    """Returns all scaffolder questions."""
    return self.QUESTIONS

  @abc.abstractmethod
  def GenerateFiles(self) -> Iterator[Tuple[str, str]]:
    """Generate all the files this scaffolder provides.

    Yields:
      list: file name and content of the file to be written to disk.
    """

  @abc.abstractmethod
  def GetFilesToCopy(self) -> Iterator[Tuple[str, str]]:
    """Return a list of files that need to be copied.

    Yields:
      tuple (str, str): file name of source and destination.
    """

  def RaiseIfNotReady(self):
    """Checks to see if all attributes are set to start generating files.

    By default this function only checks to see if all attributes defined
    in questions and Jinja2 context have values and are not empty.

    Raises:
      ScaffolderNotConfigured: if the scaffolder is not fully configured.
    """
    for question in self.GetQuestions():
      attribute = getattr(self, question.attribute, None)

      if not attribute:
        raise errors.ScaffolderNotConfigured(
            'Attribute [{0:s}] has not yet been set.'.format(
                question.attribute))

    for jinja_context_attribute in self.GetJinjaContext():
      if not jinja_context_attribute:
        raise errors.ScaffolderNotConfigured((
            'The required attribute for jinja2 template: [{0:s}] has not '
            'yet been set.').format(jinja_context_attribute))

  def SetOutputName(self, output_name: str):
    """Sets the name of the output module.

    This is the name of the generated output module this scaffolder
    implements.

    Args:
      output_name (str): the name of the output that the scaffolder generates,
          whether that is an output module, plugin, parser, analyzer or
          something else.
    """
    self._output_name = output_name

  def SetAttribute(self, name: str, value: object, value_type: type):
    """Store an attribute read from the CLI.

    Args:
      name (str): the attribute name.
      value (object): the attribute value.
      value_type (type): the attribute type.

    Raises:
      ValueError: if the value is not of the correct type.
      KeyError: If the attribute is not configured for this scaffolder.
    """
    if not hasattr(self, name):
      raise KeyError(
          'Attribute {0:s} is not configured for this scaffolder.'.format(name))

    if not isinstance(value, value_type):
      raise ValueError('Value is of type {0:s}, not {1:s}'.format(
          type(value), value_type))

    setattr(self, name, value)
