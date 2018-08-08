# -*- coding: utf-8 -*-
"""To Format the code """

from plasoscaffolder.common import base_code_formatter
from yapf.yapflib import yapf_api


class CodeFormatter(base_code_formatter.BaseCodeFormatter):
  """Class handles the code formation of files."""

  def __init__(self, yapf_path: str):
    """Initializing the code formatter.

    Args:
      yapf_path (str): the path to the yapf style file
    """
    super().__init__()
    self.yapf_path = yapf_path

  def Format(self, code: str) -> str:
    """Formats the code.

    Args:
      code (str): the code to format

    Returns:
      str: the formatted code
    """
    return yapf_api.FormatCode(code, style_config=self.yapf_path)
