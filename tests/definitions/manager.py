# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test class for the definition manager."""
import unittest

from l2tscaffolder.definitions import interface
from l2tscaffolder.definitions import manager


class GoldTestProject(interface.ScaffolderDefinition):
  """Test project."""

  NAME = 'gold'

  def ValidatePath(self, root_path: str) -> bool:
    """Validates the path to the root directory of the project.

    Args:
      root_path (str): path to a project source tree.

    Returns:
      bool: true if the path contains 'gold'.
    """
    if 'gold' in root_path:
      return True

    return False


class SilverTestProject(interface.ScaffolderDefinition):
  """Test project."""

  NAME = 'silver'

  def ValidatePath(self, root_path: str) -> bool:
    """Validates the path to the root directory of the project.

    Args:
      root_path (str): path to a project source tree.

    Returns:
      bool: true if the path contains 'gold'.
    """
    if 'silver' in root_path:
      return True

    return False


class FailingTestProject(interface.ScaffolderDefinition):
  """Test project that always fails."""

  NAME = 'failing'

  def ValidatePath(self, root_path: str) -> bool:
    """Test validation.

    Args:
      root_path (str): path to a project source tree.

    Returns:
      bool: always False, for testing.
    """
    return False


class DefinitionManagerTest(unittest.TestCase):
  """Test case for the definition manager. """

  @classmethod
  def setUpClass(cls):
    """Sets up the test class."""
    # Need to make sure there are no registered projects, and can't iterate
    # directly over projects since changing the dict in the middle of an iter
    # causes errors.
    registered_definitions = list(
        manager.DefinitionManager.GetDefinitionObjects())
    for definition_object in registered_definitions:
      registered_class = type(definition_object)
      manager.DefinitionManager.DeregisterDefinition(registered_class)

    manager.DefinitionManager.RegisterDefinition(GoldTestProject)
    manager.DefinitionManager.RegisterDefinition(FailingTestProject)

  def testGetDefinitionByName(self):
    """Test getting definitions by name."""
    test_definition = manager.DefinitionManager.GetDefinitionByName(
        GoldTestProject.NAME)

    self.assertEqual(test_definition.NAME, GoldTestProject.NAME)

    test_definition = manager.DefinitionManager.GetDefinitionByName(
        'DoesNotExist')

    self.assertEqual(test_definition, None)

  def testRegisteringAndDeregistering(self):
    """Test registering and deregistering definitions."""
    definitions = list(manager.DefinitionManager.GetDefinitionNames())
    self.assertEqual(len(definitions), 2)

    manager.DefinitionManager.RegisterDefinition(SilverTestProject)
    self.assertEqual(
        len(list(manager.DefinitionManager.GetDefinitionNames())), 3)

    with self.assertRaises(KeyError):
      manager.DefinitionManager.RegisterDefinition(SilverTestProject)

    manager.DefinitionManager.DeregisterDefinition(SilverTestProject)
    self.assertEqual(
        len(list(manager.DefinitionManager.GetDefinitionNames())), 2)

  def testGetDefinitionNames(self):
    """Test getting definition names."""
    definitions = list(manager.DefinitionManager.GetDefinitionNames())

    self.assertEqual(len(definitions), 2)
    correct_definitions = ['gold', 'failing']

    self.assertSetEqual(set(definitions), set(correct_definitions))


if __name__ == '__main__':
  unittest.main()
