# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test class for the project manager."""
import unittest

from plasoscaffolder.projects import manager

from tests.projects import test_helper


class ProjectManagerTest(unittest.TestCase):
  """Test case for the project manager. """

  @classmethod
  def setUpClass(cls):
    # Need to make sure there are no registered projects, and can't iterate
    # directly over projects since changing the dict in the middle of an iter
    # causes errors.
    existing_projects = list(manager.ProjectManager.GetProjectObjects())
    for project_class in existing_projects:
      manager.ProjectManager.DeregisterPlugin(project_class)

    manager.ProjectManager.RegisterProject(test_helper.TestProject)
    manager.ProjectManager.RegisterProject(test_helper.TestProjectFails)

  def testRegisteringAndDeregistering(self):
    """Test registering and deregistering projects."""
    projects = list(manager.ProjectManager.GetProjectNames())
    self.assertEqual(len(projects), 2)

    manager.ProjectManager.RegisterProject(test_helper.SecondTestProject)
    self.assertEqual(len(list(manager.ProjectManager.GetProjectNames())), 3)

    with self.assertRaises(KeyError):
      manager.ProjectManager.RegisterProject(test_helper.SecondTestProject)

    manager.ProjectManager.DeregisterPlugin(test_helper.SecondTestProject)
    self.assertEqual(len(list(manager.ProjectManager.GetProjectNames())), 2)

  def testGetProjectNames(self):
    """Test getting project names."""
    projects = list(manager.ProjectManager.GetProjectNames())

    self.assertEquals(len(projects), 2)
    correct_projects = ['stranger', 'failing']

    self.assertSetEqual(set(projects), set(correct_projects))


if __name__ == '__main__':
  unittest.main()
