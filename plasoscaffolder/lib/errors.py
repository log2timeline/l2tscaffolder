# -*- coding: utf-8 -*-
"""This file contains the error classes."""


class Error(Exception):
  """Base error class."""


class NoValidDefinition(Error):
  """Raised when no valid project has been identified."""


class EngineNotConfigured(Error):
  """Raised when the scaffolder engine has not been configured correctly."""

class ScaffolderNotConfigured(Error):
  """Raised when the scaffolder has not been configured correctly."""
