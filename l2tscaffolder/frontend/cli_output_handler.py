# -*- coding: utf-8 -*-
"""The output file handler for click"""
import click

from l2tscaffolder.frontend import output_handler


class OutputHandlerClick(output_handler.BaseOutputHandler):
  """Output handler for click."""

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
    return click.confirm(text, abort=abort, default=default)

  def PrintError(self, text: str):
    """Presents an error message.

    Args:
      text (str): the error message to present.
    """
    click.secho(text, fg='red', bold=True)

  def PrintInfo(self, text: str):
    """Presents the user with an informational text.

    Args:
      text (str): the text to present.
    """
    click.secho(text, fg='cyan')

  def PrintNewLine(self):
    """Adds a new or blank line to the output."""
    click.echo('')

  def PrintOutput(self, text: str):
    """Presents the user with output from the tool.

    Args:
      text (str): the text to present the user with.
    """
    click.secho(text, fg='yellow', bold=True)

  def PromptError(self, text: str) -> str:
    """Presents the user with an error message and return back the answer.

    Args:
      text (str): the text to prompt

    Returns:
      str: the user input
    """
    return click.prompt(click.style(text, fg='red'), type=str)

  def PromptInfo(self, text: str) -> str:
    """Presents the user with a message prompt and return back the answer.

    Args:
      text (str): the text to prompt

    Returns:
      str: the user input
    """
    return click.prompt(text, type=str)

  def PromptInfoWithDefault(self, text: str, input_type: type,
                            default: object) -> object:
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
    return click.prompt(text, type=input_type, default=default)
