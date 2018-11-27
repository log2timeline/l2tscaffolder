# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test class for the file handler."""
import filecmp
import os
import tempfile
import unittest

from l2tscaffolder.lib import file_handler


class FileHandlerTest(unittest.TestCase):
  """Tests for the FileHandler class."""
  name = "__testfile"
  suffix = "py"
  file = '{0:s}.{1:s}'.format(name, suffix)
  maxDiff = None

  def testCreateFolder(self):
    """Tests if the creation of a folder works."""
    with tempfile.TemporaryDirectory() as directory:
      new_path = os.path.join(directory, "newfolder")
      self.assertFalse(os.path.exists(new_path))
      handler = file_handler.FileHandler()
      handler._CreateFolder(new_path)  # pylint: disable=protected-access
      actual = os.path.exists(new_path)
    self.assertTrue(actual)

  def testCreateFilePath(self):
    """Tests if the construction of the folder path works."""
    with tempfile.TemporaryDirectory() as directory:
      new_path = os.path.join(directory, "temp")
      path = file_handler.FileHandler.CreateFilePath(
          new_path, self.name, self.suffix)
      self.assertEqual(path, os.path.join(new_path, self.file))

  def testCreateFile(self):
    """Tests if the creation of a file none existing beforehand works."""
    with tempfile.TemporaryDirectory() as directory:
      handler = file_handler.FileHandler()
      file_path = os.path.join(directory, self.file)
      self.assertFalse(os.path.exists(file_path))
      handler.CreateFile(directory, self.name, self.suffix)
      self.assertTrue(os.path.exists(file_path))

  def testCreateFileIfPathNotExisting(self):
    """Tests creation of non-existing file."""
    with tempfile.TemporaryDirectory() as directory:
      new_path = os.path.join(directory, "temp")
      handler = file_handler.FileHandler()
      file_path = os.path.join(new_path, self.file)
      self.assertFalse(os.path.exists(file_path))
      handler.CreateFile(new_path, self.name, self.suffix)
      self.assertTrue(os.path.exists(file_path))

  def testCreateFileFromPath(self):
    """Tests if the creation of a file none existing beforehand works."""
    handler = file_handler.FileHandler()
    with tempfile.TemporaryDirectory() as directory:
      source = os.path.join(directory, self.file)
      self.assertFalse(os.path.exists(source))
      handler.CreateFileFromPath(source)
      self.assertTrue(os.path.exists(source))

  def testCopyFile(self):
    """Tests if the copying of a file none existing beforehand works."""
    expected_content = "this is test content."

    with tempfile.TemporaryDirectory() as directory:
      source = os.path.join(directory, self.file)
      destination = os.path.join(directory, "copy", self.file)

      with open(source, "a") as f:
        f.write(expected_content)

      handler = file_handler.FileHandler()
      self.assertFalse(os.path.exists(destination))
      handler.CopyFile(source, destination)
      self.assertTrue(os.path.exists(destination))
      self.assertTrue(filecmp.cmp(destination, source))

  def testAddContentIfFileExists(self):
    """Tests if the editing of a file existing works."""
    content = "this is test content. "
    expected = content + content

    with tempfile.TemporaryDirectory() as directory:
      source = os.path.join(directory, self.file)
      with open(source, "a") as f:
        f.write(content)

      handler = file_handler.FileHandler()
      self.assertTrue(os.path.exists(source))
      handler.AddContent(source, content)
      self.assertTrue(os.path.exists(source))

      with open(source, "r") as f:
        actual = f.read()

    self.assertEqual(expected, actual)

  def testAddContentIfFileDoesNotExist(self):
    """Tests if the editing of a file not existing works."""
    content = "this is test content. "
    expected = content

    with tempfile.TemporaryDirectory() as directory:
      source = os.path.join(directory, self.file)
      handler = file_handler.FileHandler()
      self.assertFalse(os.path.exists(source))
      handler.AddContent(source, content)
      self.assertTrue(os.path.exists(source))

      with open(source, "r") as f:
        actual = f.read()

    self.assertEqual(expected, actual)

  def testCreateOrModifyFileWithContentIfFileExists(self):
    """Tests creation or modification of existing file with content."""
    content = "this is test content. "
    expected = content + content

    with tempfile.TemporaryDirectory() as directory:
      source = os.path.join(directory, self.file)
      with open(source, "a") as f:
        f.write(content)

      handler = file_handler.FileHandler()
      self.assertTrue(os.path.exists(source))
      handler.CreateOrModifyFileWithContent(source, content)
      self.assertTrue(os.path.exists(source))

      with open(source, "r") as f:
        actual = f.read()

    self.assertEqual(expected, actual)

  def testAddContentIfFileAndFolderDoesNotExist(self):
    """Tests creation or modification of non-existing file with content."""
    content = "this is test content. "
    expected = content

    with tempfile.TemporaryDirectory() as directory:
      new_path = os.path.join(directory, "newfolder")
      source = os.path.join(new_path, self.file)
      handler = file_handler.FileHandler()
      self.assertFalse(os.path.exists(source))
      handler.CreateOrModifyFileWithContent(source, content)
      self.assertTrue(os.path.exists(source))

      with open(source, "r") as f:
        actual = f.read()

    self.assertEqual(expected, actual)

  def testAddImportToInit(self):
    """Tests adding a line to an init file."""
    test_path = os.path.join(os.path.dirname(
        os.path.dirname(os.path.dirname(__file__))), 'test_data')
    test_file = os.path.join(test_path, 'test_init.py')

    with open(test_file, 'r') as fh:
      test_file_content = fh.read()

    new_import = 'from secret.project.parsers import foobar\n'

    temp_file = tempfile.NamedTemporaryFile()
    with open(temp_file.name, 'w') as fh:
      fh.write(test_file_content)

    handler = file_handler.FileHandler()
    handler.AddImportToInit(temp_file.name, new_import)

    with open(temp_file.name, 'r') as fh:
      content = fh.read()
    os.remove(temp_file.name)

    expected_file_path = os.path.join(test_path, 'test_init_fixed.py')
    with open(expected_file_path, 'r') as fh:
      expected_content = fh.read()

    self.assertEqual(content, expected_content)


if __name__ == '__main__':
  unittest.main()
