# -*- coding: utf-8 -*-
"""base output handler"""
import abc


class BaseOutputHandler(object):
  """Base class representing the Base class for the output handler class"""
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def PromptInfo(self, text: str) -> str:
    """A prompt for information.

    Args:
      text (str): the text to prompt

    Returns:
      str: the user input
    """

  @abc.abstractmethod
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

  @abc.abstractmethod
  def PromptError(self, text: str) -> str:
    """A prompt for errors.

    Args:
      text (str): the text to prompt

    Returns:
      str: the user input
    """

  @abc.abstractmethod
  def PrintInfo(self, text: str):
    """An echo for information.

    Args:
      text (str): the text to print
    """

  @abc.abstractmethod
  def PrintError(self, text: str):
    """An echo for errors.

    Args:
      text (str): the text to print
    """

  @abc.abstractmethod
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
