# -*- coding: utf-8 -*-
"""The plugin interface classes."""
import abc
import collections

from plasoscaffolder.lib import definitions
from plasoscaffolder.lib import errors


Question = collections.namedtuple(
    'question', ['attribute', 'prompt', 'help', 'type'])


class ScaffolderPlugin(object):
  """The plugin interface."""

  # The name of the plugin or parser this scaffolder plugin provides.
  NAME = 'base_parser'

  # One liner describing what the plugin provides.
  DESCRIPTION = ''

  # Define which project this particular plugin belongs to.
  PROJECT = definitions.PROJECT_UNDEFINED

  # Questions, a list that contains all the needed questions that the
  # user should be prompted about before the plugin or parser is created.
  # Each element in the list should be of the named tuple question.
  QUESTIONS = []

  def __init__(self):
    """Initializes the plugin."""
    super(ScaffolderPlugin, self).__init__()
    self._attributes = {}
    self._defined_attributes = set()
    self._output_name = ''

  def GetQuestions(self) -> list:
    """Returns all plugin questions."""
    return self.QUESTIONS

  @abc.abstractmethod
  def GenerateFiles(self) -> (str, str):
    """Generate all the files this plugin provides.

    Yields:
      list: file name and content of the file to be written to disk.
    """

  @abc.abstractmethod
  def GetFilesToCopy(self) -> (str, str):
    """Return a list of files that need to be copied.

    Yields:
      list (str, str): file name of source and destination.
    """

  def IsPluginConfigured(self):
    """Check to see if all attributes are set to start generating files.

    Raises:
      PluginNotConfigured: if the plugin is not fully configured.
    """
    configured_attributes = set(self._attributes.keys())
    if configured_attributes != self._defined_attributes:
      mismatch = self._defined_attributes.difference(self._attributes)
      raise errors.PluginNotConfigured((
          'Not all required attributes have been defined, the following '
          'attributes are missing: {}').format(
              ','.join(str(x) for x in mismatch)))

  def SetOutputName(self, output_name: str):
    """Sets the name of the output module.

    Args:
      output_name (str): the name of the output that the plugin provides,
          whether that is an output module, plugin, parser,
          analyzer or something else.
    """
    self._output_name = output_name

  def SetAttribute(self, name: str, value: object, value_type: object):
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

  def SetupPlugin(self):
    """Sets up the plugin."""
    for question in self.GetQuestions():
      self._defined_attributes.add(question.attribute)
