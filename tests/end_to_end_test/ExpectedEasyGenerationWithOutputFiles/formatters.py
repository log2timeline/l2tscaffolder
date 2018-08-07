# -*- coding: utf-8 -*-
"""test database formatter."""

from plaso.formatters import interface
from plaso.formatters import manager
from plaso.lib import errors


class TestUsersFormatter(interface.ConditionalEventFormatter):
  """test users event formatter."""

  DATA_TYPE = u'test:'
  """Correct Format String Pieces where needed"""

  FORMAT_STRING_PIECES = [
    u'Id:{id}',
    u'Name:{name}']

  #TODO: remove Format String Pieces for the short Format
  FORMAT_STRING_SHORT_PIECES = [
    u'Id:{id}',
    u'Name:{name}']

  SOURCE_LONG = u'Test Users'
  SOURCE_SHORT = u'Test'


manager.FormattersManager.RegisterFormatter([TestUsersFormatter])
