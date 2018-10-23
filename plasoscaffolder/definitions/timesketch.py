# -*- coding: utf-8 -*-
"""The Timesketch definition class."""

import os

from plasoscaffolder.lib import definitions
from plasoscaffolder.definitions import interface
from plasoscaffolder.definitions import manager

class TimesketchProject(interface.ScaffolderDefinition):
  """Timesketch project definition."""

  NAME = definitions.DEFINITION_TIMESKETCH

  def ValidatePath(self, root_path: str) -> bool:
    """Validates the path to a Timesketch development tree.

    Args:
      root_path (str): the path to the root of the project directory.

    Returns:
      bool: whether the given path is the correct root path to a Timesketch
          development tree.
    """
    if not os.path.isdir(root_path):
      return False

    if not os.path.isdir(os.path.join(root_path, 'timesketch')):
      return False

    if not os.path.isfile(os.path.join(root_path, 'timesketch.conf')):
      return False

    if not os.path.isdir(os.path.join(root_path, 'timesketch', 'views')):
      return False

    return True


manager.DefinitionManager.RegisterDefinition(TimesketchProject)
