# -*- coding: utf-8 -*-
"""The file handler."""
import os
import pathlib
import shutil

from l2tscaffolder.lib import errors


class FileHandler:
  """Handles the creation of files."""

  def AddImportToInit(self, path: str, entry: str):
    """Adds an import into an init file in the correct order.

    Args:
      path (str): path to the __init__ file.
      entry (str): the import statement.
    """
    if not os.path.isfile(path):
      return

    with open(path, 'r') as file_object:
      lines = file_object.readlines()

    line_index = 0
    for index, line in enumerate(lines):
      if not line.startswith('from '):
        continue
      if line > entry:
        line_index = index
        break

    if line_index:
      lines.insert(line_index, entry)
    else:
      lines.append(entry)

    with open(path, 'w') as file_object:
      for line in lines:
        file_object.write(line)

  @classmethod
  def CreateFilePath(cls, path: str, name: str, extension: str) -> str:
    """Creates the file path from the directory path, filename and suffix.

    Args:
      path (str): path to the file directory.
      name (str): filename.
      extension (str): file extension.

    Returns:
      str: the path to the file.
    """
    file_name = '{0:s}.{1:s}'.format(name, extension)
    return os.path.join(path, file_name)

  @classmethod
  def _CreateFolder(cls, directory_path: str):
    """Creates a folder.

     This function should only to be called if the target folder does not yet
     exist or there will be an exception.

     Args:
       directory_path (str): path to the directory to create.
     """
    os.makedirs(directory_path)

  def CreateFile(
      self, directory_path: str, file_name: str,
      filename_extension: str) -> str:
    """Creates a empty file.

    Args:
      directory_path (str): path to the directory the file should be created in.
      file_name (str): name of the new file.
      filename_extension (str): extension of the new file.

    Returns:
      str: path of the created file
    """
    file_path = self.CreateFilePath(
        directory_path, file_name, filename_extension)

    if not os.path.exists(directory_path):
      self._CreateFolder(directory_path)

    pathlib.Path(file_path).touch()
    return file_path

  def CreateFileFromPath(self, file_path: str) -> str:
    """Creates a empty file.

    Args:
      file_path (str): path to the file.

    Returns:
      str: the path of the created file
    """
    _ = self.CreateFolderForFilePathIfNotExist(file_path)
    pathlib.Path(file_path).touch()
    return file_path

  def CopyFile(self, source: str, destination: str) -> str:
    """Copies a file.

    Args:
      source (str): path of the file to copy
      destination (str): path to copy the file to.

    Returns:
      str: the path of the copied file

    Raises:
      errors.FileHandlingError: when file copy operation fails.
    """
    _ = self.CreateFolderForFilePathIfNotExist(destination)
    try:
      shutil.copyfile(source, destination)
    except shutil.SameFileError as exception:
      raise errors.FileHandlingError((
          'Unable to copy file source and dest are the same files. '
          'Original error message: {0:s}').format(exception))
    except OSError as exception:
      raise errors.FileHandlingError(
          'Unable to copy file, error message: {0:s}'.format(exception))

    return destination

  def CreateOrModifyFileWithContent(self, source: str, content: str):
    """Adds content to a file and create the file and path if non existing.

    Args:
      source (str): path of the file to edit.
      content (str): content to append to the file.

    Returns:
      str: path of the edited file.
    """
    _ = self.CreateFolderForFilePathIfNotExist(source)
    return self.AddContent(source, content)

  def AddContent(self, source: str, content: str) -> str:
    """Adds content to a file and create file if non existing.

    Args:
      source (str): path of the file to edit.
      content (str): content to append to the file.

    Returns:
      str: path of the edited file.
    """
    _ = self.CreateFolderForFilePathIfNotExist(source)
    with open(source, 'a') as file_object:
      file_object.write(str(content))

    return source

  def CreateFolderForFilePathIfNotExist(self, file_path: str) -> str:
    """Creates folders for the given file if it does not exist.

    Args:
      file_path (str):  path to the file

    Returns:
      str: directory path of the created directory
    """
    directory_path = os.path.dirname(file_path)
    if not os.path.exists(directory_path):
      self._CreateFolder(directory_path)
    return directory_path
