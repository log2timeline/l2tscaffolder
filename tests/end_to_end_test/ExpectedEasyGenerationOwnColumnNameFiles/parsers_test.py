# -*- coding: utf-8 -*-
"""Tests for test plugin."""
import unittest

from plaso.lib import eventdata
from plaso.lib import timelib
from plaso.parsers.sqlite_plugins import test

from tests import test_lib as shared_test_lib
from tests.parsers.sqlite_plugins import test_lib


class TestTest(test_lib.SQLitePluginTestCase):
  """Tests for test database plugin."""

  @shared_test_lib.skipUnlessHasTestFile([u'test.db'])
  def testProcess(self):
    """Test the Process function on a Test file."""
    plugin_object = test.TestPlugin()
    storage_writer = self._ParseDatabaseFileWithPlugin([u'test.db'],
                                                       plugin_object)

    # We should have 50 events in total.
    # - 25 Users createdDate events.
    # - 25 Users updatedAt events.

    self.assertEqual(50, len(storage_writer.events))

    # Test the first users updatedAt event.
    guessed_event = [
        e for e in storage_writer.events
        if e.advertiser_account_type == u'0' and e.analytics_type == u'0' and
        e.bio_entities == u'None' and e.business_profile_state == u'0' and
        e.could_be_stale == u'0' and e.description ==
        u'Breaking news alerts and updates from the BBC. For news,'
        u'features, analysis follow @BBCWorld (international) or @BBCNews'
        u'(UK). Latest sport news @BBCSport.' and e.device_following == u'0' and
        e.extended_profile_fields == u'None' and e.favorites_count == u'0' and
        e.followers_count == u'19466932' and e.followers_count_fast == u'0' and
        e.followers_count_normal == u'0' and e.following == u'0' and
        e.following_count == u'3' and e.has_collections == u'0' and
        e.has_extended_profile_fields == u'0' and e.id == u'5402612' and
        e.is_lifeline_institution == u'0' and e.is_translator == u'0' and
        e.location == u'London, UK' and e.media_count == u'None' and
        e.name == u'BBC Breaking News' and e.pinned_tweet_id == u'None' and
        e.profile_banner_url ==
        u'https://pbs.twimg.com/profile_banners/5402612/1398336837' and
        e.profile_image_url ==
        u'https://pbs.twimg.com/profile_images/460740982498013184/wIPwMwru'
        u'_normal.png' and e.profile_link_color_hex_triplet == u'2052731' and
        e.protected == u'0' and e.screen_name == u'BBCBreaking' and
        e.statuses_count == u'26697' and e.structured_location == u'None' and
        e.url == u'http://www.bbc.co.uk/news' and e.url_entities == u'None' and
        e.verified == u'1'
    ][0]
    position = storage_writer.index(guessed_event)
    test_event = storage_writer.events[position]

    expected_timestamp = timelib.Timestamp.CopyFromString(u'1449070544.333328')
    self.assertEqual(test_event.timestamp, expected_timestamp)

    self.assertEqual(
        test_event.timestamp_desc, eventdata.EventTimestamp.CREATION_TIME)
    self.assertEqual(test_event.advertiser_account_type, u'0')
    self.assertEqual(test_event.analytics_type, u'0')
    self.assertEqual(test_event.bio_entities, u'None')
    self.assertEqual(test_event.business_profile_state, u'0')
    self.assertEqual(test_event.could_be_stale, u'0')
    expected_description = (
        u'Breaking news alerts and updates from the BBC. For news,'
        u'features, analysis follow @BBCWorld (international) or @BBCNews'
        u'(UK). Latest sport news @BBCSport.')
    self.assertEqual(test_event.description, expected_description)
    self.assertEqual(test_event.device_following, u'0')
    self.assertEqual(test_event.extended_profile_fields, u'None')
    self.assertEqual(test_event.favorites_count, u'0')
    self.assertEqual(test_event.followers_count, u'19466932')
    self.assertEqual(test_event.followers_count_fast, u'0')
    self.assertEqual(test_event.followers_count_normal, u'0')
    self.assertEqual(test_event.following, u'0')
    self.assertEqual(test_event.following_count, u'3')
    self.assertEqual(test_event.has_collections, u'0')
    self.assertEqual(test_event.has_extended_profile_fields, u'0')
    self.assertEqual(test_event.id, u'5402612')
    self.assertEqual(test_event.is_lifeline_institution, u'0')
    self.assertEqual(test_event.is_translator, u'0')
    self.assertEqual(test_event.location, u'London, UK')
    self.assertEqual(test_event.media_count, u'None')
    self.assertEqual(test_event.name, u'BBC Breaking News')
    self.assertEqual(test_event.pinned_tweet_id, u'None')
    expected_profile_banner_url = (
        u'https://pbs.twimg.com/profile_banners/5402612/1398336837')
    self.assertEqual(test_event.profile_banner_url, expected_profile_banner_url)
    expected_profile_image_url = (
        u'https://pbs.twimg.com/profile_images/460740982498013184/wIPwMwru'
        u'_normal.png')
    self.assertEqual(test_event.profile_image_url, expected_profile_image_url)
    self.assertEqual(test_event.profile_link_color_hex_triplet, u'2052731')
    self.assertEqual(test_event.protected, u'0')
    self.assertEqual(test_event.screen_name, u'BBCBreaking')
    self.assertEqual(test_event.statuses_count, u'26697')
    self.assertEqual(test_event.structured_location, u'None')
    self.assertEqual(test_event.url, u'http://www.bbc.co.uk/news')
    self.assertEqual(test_event.url_entities, u'None')
    self.assertEqual(test_event.verified, u'1')

    expected_message = (
        u'Id: 5402612 Screen Name: BBCBreaking Profile Image Url: https://'
        u'pbs.twimg.com/profile_images/460740982498013184/wIPwMwru_normal.'
        u'png Profile Banner Url:'
        u'https://pbs.twimg.com/profile_banners/5402612/1398336837 Profile'
        u'Link Color Hex Triplet: 2052731 Name: BBC Breaking News'
        u'Location: London, UK Structured Location: None Description:'
        u'Breaking news alerts and updates from the BBC. For news,'
        u'features, analysis follow @BBCWorld (international) or @BBCNews'
        u'(UK). Latest sport news @BBCSport. Url:'
        u'http://www.bbc.co.uk/news Url Entities: None Bio Entities: None'
        u'Protected: 0 Verified: 1 Following: 0 Device Following: 0'
        u'Advertiser Account Type: 0 Statuses Count: 26697 Media Count:'
        u'None Favorites Count: 0 Following Count: 3 Followers Count:'
        u'19466932 Followers Count Fast: 0 Followers Count Normal: 0 Could'
        u'Be Stale: 0 Is Lifeline Institution: 0 Has Collections: 0 Is'
        u'Translator: 0 Has Extended Profile Fields: 0 Extended Profile'
        u'Fields: None Pinned Tweet Id: None Business Profile State: 0'
        u'Analytics Type: 0')
    expected_message_short = (
        u'Id: 5402612 Screen Name: BBCBreaking Profile Image Url:'
        u'https://pbs.twimg.com...')

    self._TestGetMessageStrings(
        test_event, expected_message, expected_message_short)

    # Test the first users createdDate event.
    guessed_event = [
        e for e in storage_writer.events
        if e.advertiser_account_type == u'0' and e.analytics_type == u'0' and
        e.bio_entities == u'b&#39;{}&#39;' and e.business_profile_state == u'0'
        and e.could_be_stale == u'0' and e.description ==
        u'How people build software' and e.device_following == u'0' and
        e.extended_profile_fields == u'None' and e.favorites_count == u'155' and
        e.followers_count == u'742086' and e.followers_count_fast == u'0' and
        e.followers_count_normal == u'742086' and e.following == u'0' and
        e.following_count == u'172' and e.has_collections == u'0' and
        e.has_extended_profile_fields == u'0' and e.id == u'13334762' and
        e.is_lifeline_institution == u'0' and e.is_translator == u'0' and
        e.location == u'San Francisco, CA' and e.media_count == u'33' and e.name
        == u'GitHub' and e.pinned_tweet_id == u'None' and e.profile_banner_url
        == u'https://pbs.twimg.com/profile_banners/13334762/1415719104' and
        e.profile_image_url ==
        u'https://pbs.twimg.com/profile_images/616309728688238592/pBeeJQDQ'
        u'_normal.png' and e.profile_link_color_hex_triplet == u'255' and
        e.protected == u'0' and e.screen_name == u'github' and
        e.statuses_count == u'3120' and e.structured_location == u'None' and
        e.url == u'https://t.co/FoKGHcCyJJ' and e.url_entities ==
        u'b&#39;{&#34;urls&#34;:[{&#34;url&#34;:&#34;https:\\/\\/t.co\\/Fo'
        u'KGHcCyJJ&#34;,&#34;rangeInDisplay.length&#34;:0,&#34;displayURL&'
        u'#34;:&#34;github.com&#34;,&#34;rangeInDisplay.location&#34;:0,&#'
        u'34;expandedURL&#34;:&#34;https:\\/\\/github.com&#34;,&#34;range.'
        u'location&#34;:0,&#34;range.length&#34;:23}]}&#39;' and
        e.verified == u'1'
    ][0]
    position = storage_writer.index(guessed_event)
    test_event = storage_writer.events[position]

    expected_timestamp = timelib.Timestamp.CopyFromString(u'1202704910.0')
    self.assertEqual(test_event.timestamp, expected_timestamp)

    self.assertEqual(
        test_event.timestamp_desc, eventdata.EventTimestamp.CREATION_TIME)
    self.assertEqual(test_event.advertiser_account_type, u'0')
    self.assertEqual(test_event.analytics_type, u'0')
    self.assertEqual(test_event.bio_entities, u'b&#39;{}&#39;')
    self.assertEqual(test_event.business_profile_state, u'0')
    self.assertEqual(test_event.could_be_stale, u'0')
    self.assertEqual(test_event.description, u'How people build software')
    self.assertEqual(test_event.device_following, u'0')
    self.assertEqual(test_event.extended_profile_fields, u'None')
    self.assertEqual(test_event.favorites_count, u'155')
    self.assertEqual(test_event.followers_count, u'742086')
    self.assertEqual(test_event.followers_count_fast, u'0')
    self.assertEqual(test_event.followers_count_normal, u'742086')
    self.assertEqual(test_event.following, u'0')
    self.assertEqual(test_event.following_count, u'172')
    self.assertEqual(test_event.has_collections, u'0')
    self.assertEqual(test_event.has_extended_profile_fields, u'0')
    self.assertEqual(test_event.id, u'13334762')
    self.assertEqual(test_event.is_lifeline_institution, u'0')
    self.assertEqual(test_event.is_translator, u'0')
    self.assertEqual(test_event.location, u'San Francisco, CA')
    self.assertEqual(test_event.media_count, u'33')
    self.assertEqual(test_event.name, u'GitHub')
    self.assertEqual(test_event.pinned_tweet_id, u'None')
    expected_profile_banner_url = (
        u'https://pbs.twimg.com/profile_banners/13334762/1415719104')
    self.assertEqual(test_event.profile_banner_url, expected_profile_banner_url)
    expected_profile_image_url = (
        u'https://pbs.twimg.com/profile_images/616309728688238592/pBeeJQDQ'
        u'_normal.png')
    self.assertEqual(test_event.profile_image_url, expected_profile_image_url)
    self.assertEqual(test_event.profile_link_color_hex_triplet, u'255')
    self.assertEqual(test_event.protected, u'0')
    self.assertEqual(test_event.screen_name, u'github')
    self.assertEqual(test_event.statuses_count, u'3120')
    self.assertEqual(test_event.structured_location, u'None')
    self.assertEqual(test_event.url, u'https://t.co/FoKGHcCyJJ')
    expected_url_entities = (
        u'b&#39;{&#34;urls&#34;:[{&#34;url&#34;:&#34;https:\\/\\/t.co\\/Fo'
        u'KGHcCyJJ&#34;,&#34;rangeInDisplay.length&#34;:0,&#34;displayURL&'
        u'#34;:&#34;github.com&#34;,&#34;rangeInDisplay.location&#34;:0,&#'
        u'34;expandedURL&#34;:&#34;https:\\/\\/github.com&#34;,&#34;range.'
        u'location&#34;:0,&#34;range.length&#34;:23}]}&#39;')
    self.assertEqual(test_event.url_entities, expected_url_entities)
    self.assertEqual(test_event.verified, u'1')

    expected_message = (
        u'Id: 13334762 Screen Name: github Profile Image Url: https://pbs.'
        u'twimg.com/profile_images/616309728688238592/pBeeJQDQ_normal.png'
        u'Profile Banner Url:'
        u'https://pbs.twimg.com/profile_banners/13334762/1415719104'
        u'Profile Link Color Hex Triplet: 255 Name: GitHub Location: San'
        u'Francisco, CA Structured Location: None Description: How people'
        u'build software Url: https://t.co/FoKGHcCyJJ Url Entities: b&#39;'
        u'{&#34;urls&#34;:[{&#34;url&#34;:&#34;https:\\/\\/t.co\\/FoKGHcCy'
        u'JJ&#34;,&#34;rangeInDisplay.length&#34;:0,&#34;displayURL&#34;:&'
        u'#34;github.com&#34;,&#34;rangeInDisplay.location&#34;:0,&#34;exp'
        u'andedURL&#34;:&#34;https:\\/\\/github.com&#34;,&#34;range.locati'
        u'on&#34;:0,&#34;range.length&#34;:23}]}&#39; Bio Entities:'
        u'b&#39;{}&#39; Protected: 0 Verified: 1 Following: 0 Device'
        u'Following: 0 Advertiser Account Type: 0 Statuses Count: 3120'
        u'Media Count: 33 Favorites Count: 155 Following Count: 172'
        u'Followers Count: 742086 Followers Count Fast: 0 Followers Count'
        u'Normal: 742086 Could Be Stale: 0 Is Lifeline Institution: 0 Has'
        u'Collections: 0 Is Translator: 0 Has Extended Profile Fields: 0'
        u'Extended Profile Fields: None Pinned Tweet Id: None Business'
        u'Profile State: 0 Analytics Type: 0')
    expected_message_short = (
        u'Id: 13334762 Screen Name: github Profile Image Url:'
        u'https://pbs.twimg.com/pro...')

    self._TestGetMessageStrings(
        test_event, expected_message, expected_message_short)


if __name__ == '__main__':
  unittest.main()
