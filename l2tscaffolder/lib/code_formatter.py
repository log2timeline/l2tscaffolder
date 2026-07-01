import logging
from typing import Tuple

try:
  from yapf.yapflib import yapf_api
  HAS_YAPF = True
except ImportError:
  HAS_YAPF = False
  logging.warning('yapf not installed, code will not be formatted.')


class CodeFormatter:
  """Formats code in files."""

  def __init__(self, yapf_path: str):
    """Initializes the code formatter.

    Args:
      yapf_path (str): path to the yapf style file.
    """
    super().__init__()
    self.yapf_path = yapf_path

  def Format(self, code: str) -> Tuple[str, bool]:
    """Formats the code.

    Args:
      code (str): code to format

    Returns:
      Tuple[str, bool]: the formatted code and whether it was changed.
    """
    if not HAS_YAPF:
      return code, False
    return yapf_api.FormatCode(code, style_config=self.yapf_path)

