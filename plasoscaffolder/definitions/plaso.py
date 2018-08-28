# -*- coding: utf-8 -*-
"""The plaso definition class."""

import os

from plasoscaffolder.lib import definitions
from plasoscaffolder.definitions import interface
from plasoscaffolder.definitions import manager

class PlasoProject(interface.ScaffolderDefinition):
  """Plaso project definition."""

  NAME = definitions.DEFINITION_PLASO

  def ValidatePath(self, root_path: str) -> bool:
    """Validate the path to the root directory.

    Args:
      root_path (str): the path to the root of the project directory.

    Returns:
      (bool): determines whether the given path is the correct root path
              of the project.
    """
    if not os.path.isdir(root_path):
      return False

    if not os.path.isdir(os.path.join(root_path, 'plaso')):
      return False

    if not os.path.isfile(os.path.join(root_path, 'plaso.ini')):
      return False

    if not os.path.isdir(os.path.join(root_path, 'plaso', 'parsers')):
      return False

    return True


manager.DefinitionManager.RegisterDefinition(PlasoProject)
