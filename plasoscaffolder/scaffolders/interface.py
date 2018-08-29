# -*- coding: utf-8 -*-
"""The scaffolder interface classes."""
import abc
import collections

from typing import List
from typing import Tuple

from plasoscaffolder.lib import definitions
from plasoscaffolder.lib import errors


Question = collections.namedtuple(
    'Question', ['attribute', 'prompt', 'help', 'type'])


class Scaffolder:
  """The scaffolder interface."""

  # The name of the component/parser/submodule this scaffolder plugin generates.
  NAME = 'base_parser'

  # One liner describing what the scaffolder provides.
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
    self._attributes = {}
    self._defined_attributes = set()
    self._output_name = ''

  def GetQuestions(self) -> List[Question]:
    """Returns all scaffolder questions."""
    return self.QUESTIONS

  @abc.abstractmethod
  def GenerateFiles(self) -> Tuple[str, str]:
    """Generate all the files this scaffolder provides.

    Yields:
      list: file name and content of the file to be written to disk.
    """

  @abc.abstractmethod
  def GetFilesToCopy(self) -> Tuple[str, str]:
    """Return a list of files that need to be copied.

    Yields:
      tuple (str, str): file name of source and destination.
    """

  def RaiseIfNotReady(self):
    """Checks to see if all attributes are set to start generating files.

    Raises:
      ScaffolderNotConfigured: if the scaffolder is not fully configured.
    """
    configured_attributes = set(self._attributes.keys())
    if configured_attributes != self._defined_attributes:
      mismatch = self._defined_attributes.difference(self._attributes)
      mismatch = ','.join(str(attribute) for attribute in mismatch)
      raise errors.ScaffolderNotConfigured((
          'Not all required attributes have been defined, the following '
          'attributes are missing: {0:s}').format(mismatch))

  def SetOutputName(self, output_name: str):
    """Sets the name of the output module.

    This is the name of the generated output module this scaffolder
    implements.

    Args:
      output_name (str): the name of the output that the scaffolder provides,
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
      KeyError: If the attribute name is already defined.
    """
    if name in self._attributes:
      raise KeyError('Attribute {} already exists.'.format(name))

    if not isinstance(value, value_type):
      raise ValueError('Value is of type {0:s}, not {1:s}'.format(
          type(value), value_type))

    self._attributes[name] = value

  def SetupScaffolder(self):
    """Sets up the scaffolder."""
    for question in self.GetQuestions():
      self._defined_attributes.add(question.attribute)
