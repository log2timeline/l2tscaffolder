# -*- coding: utf-8 -*-
"""test database formatter."""

from plaso.formatters import interface
from plaso.formatters import manager
from plaso.lib import errors


class TestUsersstatusesFormatter(interface.ConditionalEventFormatter):
  """test usersstatuses event formatter."""

  DATA_TYPE = u'test:'
  """Correct Format String Pieces where needed"""

  FORMAT_STRING_PIECES = [
    u'User_Id:{user_id}']

  #TODO: remove Format String Pieces for the short Format
  FORMAT_STRING_SHORT_PIECES = [
    u'User_Id:{user_id}']

  SOURCE_LONG = u'Test Usersstatuses'
  SOURCE_SHORT = u'Test'


manager.FormattersManager.RegisterFormatter([TestUsersstatusesFormatter])
