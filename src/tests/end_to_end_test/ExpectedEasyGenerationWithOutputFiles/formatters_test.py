# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for Test event formatter."""

import unittest

from plaso.formatters import test
from tests.formatters import test_lib


class TestUsersFormatterTest(test_lib.EventFormatterTestCase):
  """Tests the Test users event formatter."""

  def testInitialization(self):
    """Tests the initialization."""
    event_formatter = test.TestUsersFormatter()
    self.assertIsNotNone(event_formatter)

  def testGetFormatStringAttributeNames(self):
    """Tests the GetFormatStringAttributeNames function."""
    event_formatter = test.TestUsersFormatter()

    expected_attribute_names = [u'id', u'name']

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)


if __name__ == '__main__':
  unittest.main()
