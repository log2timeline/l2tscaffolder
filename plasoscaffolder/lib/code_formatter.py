# -*- coding: utf-8 -*-
"""Formatter for generated code."""

from yapf.yapflib import yapf_api


class CodeFormatter:
  """Formats code in files."""

  def __init__(self, yapf_path: str):
    """Initializes the code formatter.

    Args:
      yapf_path (str): path to the yapf style file.
    """
    super().__init__()
    self.yapf_path = yapf_path

  def Format(self, code: str) -> str:
    """Formats the code.

    Args:
      code (str): code to format

    Returns:
      str: the formatted code
    """
    return yapf_api.FormatCode(code, style_config=self.yapf_path)
