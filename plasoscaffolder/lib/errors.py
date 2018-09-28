# -*- coding: utf-8 -*-
"""This file contains the error classes."""


class Error(Exception):
  """Base error class."""


class EngineNotConfigured(Error):
  """Raised when the scaffolder engine has not been configured correctly."""


class FileHandlingError(Error):
  """Raised when the file handler is unable to do file operation."""


class NoValidDefinition(Error):
  """Raised when no valid project definition has been identified."""


class ScaffolderNotConfigured(Error):
  """Raised when the scaffolder has not been configured correctly."""


class UnableToConfigure(Error):
  """Raised when the scaffolder tool has issues with configuration."""


class WrongCliInput(Error):
  """Raised when wrong input is entered into the CLI."""
