# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test class for the definition manager."""
import unittest

from plasoscaffolder.definitions import manager

from tests.definitions import test_helper


class DefinitionManagerTest(unittest.TestCase):
  """Test case for the definition manager. """

  @classmethod
  def setUpClass(cls):
    """Sets up the test class."""
    # Need to make sure there are no registered projects, and can't iterate
    # directly over projects since changing the dict in the middle of an iter
    # causes errors.
    existing_definition = list(manager.DefinitionManager.GetDefinitionObjects())
    for definition_class in existing_definition:
      manager.DefinitionManager.DeregisterDefinition(definition_class)

    manager.DefinitionManager.RegisterDefinition(test_helper.TestProject)
    manager.DefinitionManager.RegisterDefinition(test_helper.TestProjectFails)

  def testRegisteringAndDeregistering(self):
    """Test registering and deregistering definitions."""
    definitions = list(manager.DefinitionManager.GetDefinitionNames())
    self.assertEqual(len(definitions), 2)

    manager.DefinitionManager.RegisterDefinition(test_helper.SecondTestProject)
    self.assertEqual(
        len(list(manager.DefinitionManager.GetDefinitionNames())), 3)

    with self.assertRaises(KeyError):
      manager.DefinitionManager.RegisterDefinition(
          test_helper.SecondTestProject)

    manager.DefinitionManager.DeregisterDefinition(
        test_helper.SecondTestProject)
    self.assertEqual(
        len(list(manager.DefinitionManager.GetDefinitionNames())), 2)

  def testGetDefinitionNames(self):
    """Test getting definition names."""
    definitions = list(manager.DefinitionManager.GetDefinitionNames())

    self.assertEquals(len(definitions), 2)
    correct_definitions = ['stranger', 'failing']

    self.assertSetEqual(set(definitions), set(correct_definitions))


if __name__ == '__main__':
  unittest.main()
