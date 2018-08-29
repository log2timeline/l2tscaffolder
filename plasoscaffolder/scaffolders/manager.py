# -*- coding: utf-8 -*-
"""The scaffolder manager."""

from typing import Dict
from typing import List
from typing import Optional
from typing import Generator
from typing import Tuple
from typing import Type

from plasoscaffolder.scaffolders import interface


class ScaffolderManager(object):
  """The scaffolder manager."""

  _scaffolder_classes = {}

  @classmethod
  def DeregisterScaffolder(cls, scaffolder_class: Type[interface.Scaffolder]):
    """Deregisters a scaffolder class.

    The scaffolder classes are identified based on their lower case name.

    Args:
      scaffolder_class (type): scaffolder class (subclass of Scaffolder).

    Raises:
      KeyError: if scaffolder class is not set for the corresponding name.
    """
    scaffolder_name = scaffolder_class.NAME.lower()
    if scaffolder_name not in cls._scaffolder_classes:
      raise KeyError('Scaffolder class not set for name: {0:s}.'.format(
          scaffolder_class.NAME))

    del cls._scaffolder_classes[scaffolder_name]

  @classmethod
  def GetScaffolderNames(cls) -> Generator[str, None, None]:
    """Retrieves the scaffolder names.

    Yields:
      str: scaffolder names.
    """
    for scaffolder_name, scaffolder_class in cls.GetScaffolders():
      yield scaffolder_name

  @classmethod
  def GetScaffolderInformation(cls) -> Generator[Tuple[str, str], None, None]:
    """Retrieves the scaffolder information.

    Yields:
      tuple[str, str]: pairs of scaffolder names and descriptions.
    """
    for scaffolder_name, scaffolder_class in cls.GetScaffolders():
      yield (scaffolder_name, scaffolder_class.DESCRIPTION)

  @classmethod
  def GetScaffolderObjectByName(
      cls, scaffolder_name) -> Optional[interface.Scaffolder]:
    """Retrieves a specific scaffolder object by the component it provides.

    Args:
      scaffolder_name (str): name of the scaffolder or parser it provides.

    Returns:
      Scaffolder: scaffolder object or None.
    """
    scaffolder_class = cls._scaffolder_classes.get(scaffolder_name.lower(), None)
    if scaffolder_class:
      return scaffolder_class()
    return None

  @classmethod
  def GetScaffolderObjects(cls) -> Dict[str, Type[interface.Scaffolder]]:
    """Retrieves the scaffolder objects.

    Returns:
      dict[str, Scaffolder]: scaffolders per name.
    """
    scaffolder_objects = {}
    for scaffolder_name, scaffolder_class in cls._scaffolder_classes.items():
      scaffolder_object = scaffolder_class()
      scaffolder_objects[scaffolder_name] = scaffolder_object

    return scaffolder_objects

  @classmethod
  def GetScaffolderQuestions(cls) -> List[Type[interface.Question]]:
    """Retrieves all the questions asked by scaffolders."""
    questions = []
    for scaffolder_class in cls._scaffolder_classes.values():
      questions.extend(scaffolder_class.QUESTIONS)

    return questions

  @classmethod
  def GetScaffolderQuestionByName(cls, scaffolder_name: str) -> list:
    """Retrieve a list of questions asked by a scaffolder based on name.

    Args:
      scaffolder_name (str): name of the scaffolder or parser the scaffolder
          provides.

    Returns:
      list: a list with all the questions (namedtuple) needed to setup the
          scaffolder. If scaffolder_name is not registered an empty list will
          be returned.
    """
    scaffolder_class = cls._scaffolder_classes.get(
        scaffolder_name.lower(), None)
    if not scaffolder_class:
      return list()

    return scaffolder_class.QUESTIONS

  @classmethod
  def GetScaffolders(cls):
    """Retrieves the registered scaffolders.

    Retrieves a dictionary of all registered scaffolders.

    Yields:
      tuple: contains:

      * str: name of the scaffolder:
      * type: scaffolder class (subclass of Scaffolder).
    """
    for scaffolder_name, scaffolder_class in cls._scaffolder_classes.items():
      yield scaffolder_name, scaffolder_class

  @classmethod
  def RegisterScaffolder(cls, scaffolder_class: Type[interface.Scaffolder]):
    """Registers a scaffolder class.

    The scaffolder classes are identified based on their lower case name.

    Args:
      scaffolder_class (type): scaffolder class (subclass of Scaffolder).

    Raises:
      KeyError: if scaffolder class is already set for the corresponding name.
    """
    scaffolder_name = scaffolder_class.NAME.lower()
    if scaffolder_name in cls._scaffolder_classes:
      raise KeyError('Scaffolder class already set for name: {0:s}.'.format(
          scaffolder_class.NAME))

    cls._scaffolder_classes[scaffolder_name] = scaffolder_class

  @classmethod
  def RegisterScaffolders(
      cls, scaffolder_classes: List[Type[interface.Scaffolder]]):
    """Registers scaffolder classes.

    The scaffolder classes are identified based on their lower case name.

    Args:
      scaffolder_classes (list[type]): scaffolders classes
          (subclasses of Scaffolder).

    Raises:
      KeyError: if scaffolder class is already set for the corresponding name.
    """
    for scaffolder_class in scaffolder_classes:
      cls.RegisterScaffolder(scaffolder_class)
