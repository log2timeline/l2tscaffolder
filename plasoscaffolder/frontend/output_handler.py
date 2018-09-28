# -*- coding: utf-8 -*-
"""The output file handler for click"""
import click


class OutputHandlerClick:
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
    return click.confirm(text, abort=abort, default=default)

  def PrintError(self, text: str):
    """A echo for errors with click.

    Args:
      text (str): the text to print
    """
    click.secho(text, fg='red', bold=True)

  def PrintInfo(self, text: str):
    """A echo for information with click.

    Args:
      text (str): the text to print
    """
    click.secho(text, fg='cyan')

  def PrintNewLine(self):
    """A new line added to output."""
    click.echo('')

  def PrintOutput(self, text: str):
    """A echo for information with click.

    Args:
      text (str): the text to print.
    """
    click.secho(text, fg='yellow', bold=True)

  def PromptError(self, text: str) -> str:
    """A prompt for errors with click.

    Args:
      text (str): the text to prompt

    Returns:
      str: the user input
    """
    return click.prompt(click.style(text, fg='red'), type=str)

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
