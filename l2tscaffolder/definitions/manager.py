# -*- coding: utf-8 -*-
"""The definition manager."""

from typing import Iterator
from typing import Type

from l2tscaffolder.definitions import interface


class DefinitionManager:
  """The definition manager."""

  _definition_classes = {}

  @classmethod
  def DeregisterDefinition(
      cls, definition_class: Type[interface.ScaffolderDefinition]):
    """Deregisters a definition class.

    Definition classes are identified by their NAME attribute.

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
  def GetDefinitionByName(
      cls, name: str) -> Type[interface.ScaffolderDefinition]:
    """Returns a definition class based on registered name.

    Args:
      name (str): name of the definition.

    Returns:
      interface.ScaffolderDefinition: definition class or None
          if name is not registered.
    """
    return cls._definition_classes.get(name, None)

  @classmethod
  def GetDefinitionNames(cls) -> Iterator[str]:
    """Yields all names of registered definition classes.

    Yields:
      str: definition names.
    """
    for definition_name in cls._definition_classes:
      yield definition_name

  @classmethod
  def GetDefinitionObjects(cls) -> Iterator[interface.ScaffolderDefinition]:
    """Yields instances of each registered definition class.

    Yields:
      ScaffolderDefinition: definition object.
    """
    for definition_class in cls._definition_classes.values():
      yield definition_class()

  @classmethod
  def RegisterDefinition(
      cls, definition_class: Type[interface.ScaffolderDefinition]):
    """Registers a definition class.

    Definition classes are identified by their NAME attribute.

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
