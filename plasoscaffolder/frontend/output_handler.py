# -*- coding: utf-8 -*-
"""The output file handler."""


class BaseOutputHandler:
  """Class representing the output handler for click."""

  def Confirm(self, text: str, default=True, abort=True):
    """Ask for a confirmation, either yes or no to a question.

     Args:
       text (str): prompts the user for a confirmation, with the given test as
           the question
       default (bool): the default for the confirmation answer. If True the
           default is Y(es), if False the default is N(o)
       abort (bool): if the program should abort if the user answer to the
           confirm prompt is no. The default is an abort.

     Returns:
        bool: False if the user entered no, True if the user entered yes
     """

  def PrintError(self, text: str):
    """A echo for errors with click.

    Args:
      text (str): the text to print
    """

  def PrintInfo(self, text: str):
    """A echo for information with click.

    Args:
      text (str): the text to print
    """

  def PrintNewLine(self):
    """A new line added to output."""

  def PrintOutput(self, text: str):
    """A echo for information with click.

    Args:
      text (str): the text to print.
    """

  def PromptError(self, text: str) -> str:
    """A prompt for errors with click.

    Args:
      text (str): the text to prompt

    Returns:
      str: the user input
    """

  def PromptInfo(self, text: str) -> str:
    """A prompt for information with click.

    Args:
      text (str): the text to  prompt

    Returns:
      str: the user input
    """

  def PromptInfoWithDefault(self, text: str, text_type: object,
                            default: object) -> str:
    """A prompt for information, with a default value and a required type.

    Args:
      text (str): the text to prompt
      text_type (object): the type of the input
      default (object): the default value

    Returns:
      str: the user input
    """
