# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for The Plugin event formatter."""

import unittest

from plaso.formatters import the_plugin
from tests.formatters import test_lib


class ThePluginBlobtypesFormatterTest(test_lib.EventFormatterTestCase):
  """Tests the The Plugin blobtypes event formatter."""

  def testInitialization(self):
    """Tests the initialization."""
    event_formatter = the_plugin.ThePluginBlobtypesFormatter()
    self.assertIsNotNone(event_formatter)

  def testGetFormatStringAttributeNames(self):
    """Tests the GetFormatStringAttributeNames function."""
    event_formatter = the_plugin.ThePluginBlobtypesFormatter()

    expected_attribute_names = [u'blobval']

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)


class ThePluginIntegertypesFormatterTest(test_lib.EventFormatterTestCase):
  """Tests the The Plugin integertypes event formatter."""

  def testInitialization(self):
    """Tests the initialization."""
    event_formatter = the_plugin.ThePluginIntegertypesFormatter()
    self.assertIsNotNone(event_formatter)

  def testGetFormatStringAttributeNames(self):
    """Tests the GetFormatStringAttributeNames function."""
    event_formatter = the_plugin.ThePluginIntegertypesFormatter()

    expected_attribute_names = [
        u'bigintval', u'int2val', u'int8val', u'integerval', u'intval',
        u'mediumintval', u'smallintval', u'tinyintval', u'unsignedbigintval'
    ]

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)


class ThePluginNumerictypesFormatterTest(test_lib.EventFormatterTestCase):
  """Tests the The Plugin numerictypes event formatter."""

  def testInitialization(self):
    """Tests the initialization."""
    event_formatter = the_plugin.ThePluginNumerictypesFormatter()
    self.assertIsNotNone(event_formatter)

  def testGetFormatStringAttributeNames(self):
    """Tests the GetFormatStringAttributeNames function."""
    event_formatter = the_plugin.ThePluginNumerictypesFormatter()

    expected_attribute_names = [
        u'booleanval', u'datetimeval', u'dateval', u'decimalval', u'numericval'
    ]

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)


class ThePluginRealtypesFormatterTest(test_lib.EventFormatterTestCase):
  """Tests the The Plugin realtypes event formatter."""

  def testInitialization(self):
    """Tests the initialization."""
    event_formatter = the_plugin.ThePluginRealtypesFormatter()
    self.assertIsNotNone(event_formatter)

  def testGetFormatStringAttributeNames(self):
    """Tests the GetFormatStringAttributeNames function."""
    event_formatter = the_plugin.ThePluginRealtypesFormatter()

    expected_attribute_names = [
        u'doubleprecesionval', u'doubleval', u'floatval', u'realval'
    ]

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)


class ThePluginTexttypesFormatterTest(test_lib.EventFormatterTestCase):
  """Tests the The Plugin texttypes event formatter."""

  def testInitialization(self):
    """Tests the initialization."""
    event_formatter = the_plugin.ThePluginTexttypesFormatter()
    self.assertIsNotNone(event_formatter)

  def testGetFormatStringAttributeNames(self):
    """Tests the GetFormatStringAttributeNames function."""
    event_formatter = the_plugin.ThePluginTexttypesFormatter()

    expected_attribute_names = [
        u'characterval', u'clobval', u'nativecharacterval', u'ncharval',
        u'nvarchar_val', u'textval', u'varcharval', u'varyingcharacterval'
    ]

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)


class ThePluginNodataFormatterTest(test_lib.EventFormatterTestCase):
  """Tests the The Plugin nodata event formatter."""

  def testInitialization(self):
    """Tests the initialization."""
    event_formatter = the_plugin.ThePluginNodataFormatter()
    self.assertIsNotNone(event_formatter)

  def testGetFormatStringAttributeNames(self):
    """Tests the GetFormatStringAttributeNames function."""
    event_formatter = the_plugin.ThePluginNodataFormatter()

    expected_attribute_names = [
        u'bigintval', u'blobval', u'booleanval', u'characterval', u'clobval',
        u'datetimeval', u'dateval', u'decimalval', u'doubleprecisionval',
        u'doubleval', u'floatval', u'int2val', u'int8val', u'integerval',
        u'intval', u'mediuintval', u'nativecharacterval', u'ncharval',
        u'numericval', u'nvarcharval', u'realval', u'smallintval', u'textval',
        u'tinyintval', u'unsignedbigintval', u'varcharval',
        u'varyingcharacterval'
    ]

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)


if __name__ == '__main__':
  unittest.main()
