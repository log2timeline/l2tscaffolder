# -*- coding: utf-8 -*-
"""The output file handler for click"""
import click

from plasoscaffolder.common import base_output_handler


class OutputHandlerClick(base_output_handler.BaseOutputHandler):
  """Class representing the output handler for click."""

  def __init__(self):
    super().__init__()

  def PromptInfo(self, text: str) -> str:
    """A prompt for information with click.

    Args:
      text (str): the text to  prompt

    Returns:
      str: the user input
    """
    return click.prompt(text, type=str)

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
    return click.prompt(text, type=text_type, default=default)

  def PromptError(self, text: str) -> str:
    """A prompt for errors with click.

    Args:
      text (str): the text to prompt

    Returns:
      str: the user input
    """
    return click.prompt(click.style(text, fg='red'), type=str)

  def PrintInfo(self, text: str):
    """A echo for information with click.

    Args:
      text (str): the text to print
    """
    click.secho(text, fg='cyan')

  def PrintError(self, text: str):
    """A echo for errors with click.

    Args:
      text (str): the text to print
    """
    click.secho(text, fg='red')

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
    return click.confirm(text, abort=abort, default=default)
