# -*- coding: utf-8 -*-
"""The Turbinia definition class."""

import os

from l2tscaffolder.lib import definitions
from l2tscaffolder.definitions import interface
from l2tscaffolder.definitions import manager

class TurbiniaProject(interface.ScaffolderDefinition):
  """Turbinia project definition."""

  NAME = definitions.DEFINITION_TURBINIA

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

    if not os.path.isdir(os.path.join(root_path, 'turbinia')):
      return False

    if not os.path.isdir(os.path.join(root_path, 'terraform')):
      return False

    if not os.path.isfile(os.path.join(root_path, 'turbinia', 'evidence.py')):
      return False

    if not os.path.isdir(os.path.join(root_path, 'turbinia', 'jobs')):
      return False

    return True


manager.DefinitionManager.RegisterDefinition(TurbiniaProject)
