# -*- coding: utf-8 -*-
"""The scaffolder interface classes."""
import abc

from typing import Dict
from typing import Iterator
from typing import List
from typing import Tuple

from l2tscaffolder.lib import definitions
from l2tscaffolder.lib import errors


class BaseQuestion:
  """Scaffolder question.

  Attributes:
    attribute (str): the name of the attribute the question prompts for.
    prompt (str): help string that is displayed before the question is asked.
  """

  # The type defines the variable type this question expects
  # as an answer.
  TYPE = None

  def __init__(self, attribute: str, prompt: str):
    """Initializes the question.

    Args:
      attribute (str): the name of the attribute the question prompts for.
      prompt (str): help string that is displayed before the question is asked.
    """
    self.attribute = attribute
    self.prompt = prompt

  def _ValidateType(self, answer: object):
    """Validates the answer against the expected type.

    Args:
      answer (object): the answer to the question asked.

    Raises:
      errors.UnableToConfigure: if the answer is not the correct type.
    """
    if not isinstance(answer, self.TYPE):
      raise errors.UnableToConfigure((
          'Answer is not of the correct type. It is {0!s} '
          'instead of being {1!s}').format(type(answer)), type(self.TYPE))

  def ValidateAnswer(self, answer: object):
    """Validate an answer to a question.

    Args:
      answer (object): the answer to the question asked.

    Raises:
      errors.UnableToConfigure: if the answer is invalid.
    """
    self._ValidateType(answer)


class DictQuestion(BaseQuestion):
  """Scaffolder dict question.

  Attributes:
    attribute (str): the name of the attribute the question prompts for.
    prompt (str): help string that is displayed before the question is asked.
    key_prompt (str): the help string that is displayed before asking for each
        key.
    value_prompt (str): the help string that is displayed before asking for each
        value in the dict.
  """
  TYPE = dict

  def __init__(self, attribute, prompt, key_prompt, value_prompt):
    """Initialize the question."""
    super(DictQuestion, self).__init__(attribute, prompt)
    self.key_prompt = key_prompt
    self.value_prompt = value_prompt


class IntQuestion(BaseQuestion):
  """Scaffolder integer question."""
  TYPE = int


class ListQuestion(BaseQuestion):
  """Scaffolder list question."""
  TYPE = list


class StringQuestion(BaseQuestion):
  """Scaffolder string question."""
  TYPE = str


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
  # Each element in the list should be an instance of BaseQuestion.
  QUESTIONS = []

  def __init__(self):
    """Initializes the scaffolder."""
    super(Scaffolder, self).__init__()
    self._output_name = ''

  @abc.abstractmethod
  def GetInitFileChanges(self) -> Iterator[Tuple[str, str]]:
    """Generate a list of init files that need changing and the changes to them.

    Yields:
      tuple (str, str): path to the init file and the entry to add to it.
    """

  def GetJinjaContext(self) -> Dict[str, object]:
    """Returns a dict that can be used as a context for Jinja2 templates.

    Returns:
      dict: containing:
        str: name of Jinja argument.
        object: Jinja argument value.
    """
    return {}

  def GetQuestions(self) -> List[BaseQuestion]:
    """Returns scaffolder questions.

    Returns:
      list[BaseQuestion]: questions to prompt the user with.
    """
    return self.QUESTIONS

  @abc.abstractmethod
  def GenerateFiles(self) -> Iterator[Tuple[str, str]]:
    """Generates files this scaffolder provides.

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
            'Attribute [{0:s}] is not set.'.format(
                question.attribute))

    for jinja_context_attribute in self.GetJinjaContext():
      if not jinja_context_attribute:
        raise errors.ScaffolderNotConfigured((
            'The required attribute for jinja2 template: [{0:s}] is not '
            'set.').format(jinja_context_attribute))

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
    """Stores an attribute read from the CLI.

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
