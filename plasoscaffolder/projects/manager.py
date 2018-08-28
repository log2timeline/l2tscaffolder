# -*- coding: utf-8 -*-
"""The definition manager."""

from typing import Iterator
from typing import Type

from plasoscaffolder.projects import interface


class DefinitionManager(object):
  """The definition manager."""

  _definition_classes = {}

  @classmethod
  def DeregisterDefinition(
      cls, definition_class: Type[interface.ScaffolderDefinition]):
    """Deregisters a definition class.

    The project classes are identified based on their defined type.

    Args:
      definition_class (type): definition class (subclass of
      ScaffolderDefinition).

    Raises:
      KeyError: if definition class is not set for the corresponding name.
    """
    definition_name = definition_class.NAME

    if definition_name not in cls._definition_classes:
      raise KeyError('Definition class not set for name: {0:s}.'.format(
          definition_name))

    del cls._definition_classes[definition_name]

  @classmethod
  def GetDefinitionNames(cls) -> Iterator[str]:
    """Retrieves the definition names.

    Yields:
      str: definition names.
    """
    for project_provides in cls._definition_classes:
      yield project_provides

  @classmethod
  def GetDefinitionObjects(cls) -> Iterator[Type[interface.ScaffolderDefinition]]:
    """Retrieves the definition objects.

    Yields:
      ScaffolderDefinition: definition object.
    """
    for definition_class in cls._definition_classes.values():
      yield definition_class()

  @classmethod
  def RegisterDefinition(
      cls, definition_class: Type[interface.ScaffolderDefinition]):
    """Registers a definition class.

    The definition classes are identified based on their name.

    Args:
      definition_class (ScaffolderDefinition): definition class.

    Raises:
      KeyError: if definition class is already set for the corresponding name.
    """
    definition_name = definition_class.NAME

    if definition_name in cls._definition_classes:
      raise KeyError('Project class already set for name: {0:s}.'.format(
          definition_name))

    cls._definition_classes[definition_name] = definition_class
