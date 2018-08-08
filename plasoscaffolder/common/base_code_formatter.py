# -*- coding: utf-8 -*-
"""Base code formatter."""
import abc


class BaseCodeFormatter(object):
  """Base class representing the base class for the code formatter."""
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def Format(self, code: str) -> str:
    """Formats the code.

    Args:
      code (str): the code to format

    Returns:
      str: the formatted code.
    """
