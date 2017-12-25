# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for Test event formatter."""

import unittest

from plaso.formatters import test
from tests.formatters import test_lib


class TestUsersstatusesFormatterTest(test_lib.EventFormatterTestCase):
  """Tests the Test usersstatuses event formatter."""

  def testInitialization(self):
    """Tests the initialization."""
    event_formatter = test.TestUsersstatusesFormatter()
    self.assertIsNotNone(event_formatter)

  def testGetFormatStringAttributeNames(self):
    """Tests the GetFormatStringAttributeNames function."""
    event_formatter = test.TestUsersstatusesFormatter()

    expected_attribute_names = [u'user_id']

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)


if __name__ == '__main__':
  unittest.main()
