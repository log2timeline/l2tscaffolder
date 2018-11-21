# -*- coding: utf-8 -*-
"""The output file handler.

This file defines the interface of how an output handler should operate.
An output handler is used as a UI element, for two things:
1. Relay information back to the user.
2. Gather input from an end user and presenting it back to the tool.
"""
import abc


class BaseOutputHandler:
  """Interface for the output handler."""

  @abc.abstractmethod
  def Confirm(self, text: str, default=True, abort=True):
    """Returns a bool from a yes/no question presented to the end user.

    Args:
      text (str): the question presented to the end user.
      default (bool): the default for the confirmation answer. If True the
          default is Y(es), if False the default is N(o)
      abort (bool): if the program should abort if the user answer to the
          confirm prompt is no. The default is an abort.

    Returns:
       bool: False if the user entered no, True if the user entered yes
    """

  @abc.abstractmethod
  def PrintError(self, text: str):
    """Presents an error message.

    Args:
      text (str): the error message to present.
    """

  @abc.abstractmethod
  def PrintInfo(self, text: str):
    """Presents the user with an informational text.

    Args:
      text (str): the text to present.
    """

  @abc.abstractmethod
  def PrintNewLine(self):
    """Adds a new or blank line to the output."""

  @abc.abstractmethod
  def PrintOutput(self, text: str):
    """Presents the user with output from the tool.

    Args:
      text (str): the text to present the user with.
    """

  @abc.abstractmethod
  def PromptError(self, text: str) -> str:
    """Presents the user with an error message prompt and return back the answer.

    Args:
      text (str): the text to prompt

    Returns:
      str: the user input.
    """

  @abc.abstractmethod
  def PromptInfo(self, text: str) -> str:
    """Presents the user with a message prompt and return back the answer.

    Args:
      text (str): the text to prompt

    Returns:
      str: the user input.
    """

  @abc.abstractmethod
  def PromptInfoWithDefault(
      self, text: str, input_type: type, default: object) -> str:
    """Presents the user with a prompt with a default return value and a type.

    The prompt can have a default value to be chosen as well as a defined type
    of the returned data.

    Args:
      text (str): the text to prompt
      input_type (type): the type of the input
      default (object): the default value

    Returns:
      object: the user input, using the supplied input type.
    """
