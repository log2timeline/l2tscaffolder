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

    expected_attribute_names = [
        u'advertiser_account_type', u'analytics_type', u'bio_entities',
        u'business_profile_state', u'could_be_stale', u'description',
        u'device_following', u'extended_profile_fields', u'favorites_count',
        u'followers_count', u'followers_count_fast', u'followers_count_normal',
        u'following', u'following_count', u'has_collections',
        u'has_extended_profile_fields', u'id', u'is_lifeline_institution',
        u'is_translator', u'location', u'media_count', u'name',
        u'pinned_tweet_id', u'profile_banner_url', u'profile_image_url',
        u'profile_link_color_hex_triplet', u'protected', u'screen_name',
        u'statuses_count', u'structured_location', u'url', u'url_entities',
        u'verified'
    ]

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)


if __name__ == '__main__':
  unittest.main()
