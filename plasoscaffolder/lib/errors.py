# -*- coding: utf-8 -*-
"""This file contains the error classes."""


class Error(Exception):
  """Base error class."""


class NoValidProject(Error):
  """Raised when no valid project has been identified."""


class ScaffolderNotConfigured(Error):
  """Raised when the plugin object has not been configured correctly."""
