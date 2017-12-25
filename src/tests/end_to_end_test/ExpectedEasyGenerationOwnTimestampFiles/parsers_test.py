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

    # We should have 100 events in total.
    # - 25 Users createdDate events.
    # - 25 Users id events.
    # - 25 Users name events.
    # - 25 Users updatedAt events.

    self.assertEqual(100, len(storage_writer.events))

    # Test the first users id event.
    guessed_event = [
        e for e in storage_writer.events
        if e.advertiser_account_type == 0 and e.analytics_type == 0 and
        e.bio_entities is None and e.business_profile_state == 0 and
        e.could_be_stale == 0 and e.description ==
        u'Breaking news alerts and updates from the BBC. For news,'
        u'features, analysis follow @BBCWorld (international) or @BBCNews'
        u'(UK). Latest sport news @BBCSport.' and e.device_following == 0 and
        e.extended_profile_fields is None and e.favorites_count == 0 and
        e.followers_count == 19466932 and e.followers_count_fast == 0 and
        e.followers_count_normal == 0 and e.following == 0 and e.following_count
        == 3 and e.has_collections == 0 and e.has_extended_profile_fields == 0
        and e.is_lifeline_institution == 0 and e.is_translator == 0 and
        e.location == u'London, UK' and e.media_count is None and
        e.pinned_tweet_id is None and e.profile_banner_url ==
        u'https://pbs.twimg.com/profile_banners/5402612/1398336837' and
        e.profile_image_url ==
        u'https://pbs.twimg.com/profile_images/460740982498013184/wIPwMwru'
        u'_normal.png' and e.profile_link_color_hex_triplet == 2052731 and
        e.protected == 0 and e.screen_name == u'BBCBreaking' and
        e.statuses_count == 26697 and e.structured_location is None and
        e.url == u'http://www.bbc.co.uk/news' and e.url_entities is None and
        e.verified == 1
    ][0]
    position = storage_writer.index(guessed_event)
    test_event = storage_writer.events[position]

    # TODO add expected formatted timestamp for timestamp in database: 5402612
    expected_timestamp = timelib.Timestamp.CopyFromString(u'TODO')
    self.assertEqual(test_event.timestamp, expected_timestamp)

    self.assertEqual(
        test_event.timestamp_desc, eventdata.EventTimestamp.CREATION_TIME)
    self.assertEqual(test_event.advertiser_account_type, 0)
    self.assertEqual(test_event.analytics_type, 0)
    self.assertIsNone(test_event.bio_entities)
    self.assertEqual(test_event.business_profile_state, 0)
    self.assertEqual(test_event.could_be_stale, 0)
    expected_description = (
        u'Breaking news alerts and updates from the BBC. For news,'
        u'features, analysis follow @BBCWorld (international) or @BBCNews'
        u'(UK). Latest sport news @BBCSport.')
    self.assertEqual(test_event.description, expected_description)
    self.assertEqual(test_event.device_following, 0)
    self.assertIsNone(test_event.extended_profile_fields)
    self.assertEqual(test_event.favorites_count, 0)
    self.assertEqual(test_event.followers_count, 19466932)
    self.assertEqual(test_event.followers_count_fast, 0)
    self.assertEqual(test_event.followers_count_normal, 0)
    self.assertEqual(test_event.following, 0)
    self.assertEqual(test_event.following_count, 3)
    self.assertEqual(test_event.has_collections, 0)
    self.assertEqual(test_event.has_extended_profile_fields, 0)
    self.assertEqual(test_event.is_lifeline_institution, 0)
    self.assertEqual(test_event.is_translator, 0)
    self.assertEqual(test_event.location, u'London, UK')
    self.assertIsNone(test_event.media_count)
    self.assertIsNone(test_event.pinned_tweet_id)
    expected_profile_banner_url = (
        u'https://pbs.twimg.com/profile_banners/5402612/1398336837')
    self.assertEqual(test_event.profile_banner_url, expected_profile_banner_url)
    expected_profile_image_url = (
        u'https://pbs.twimg.com/profile_images/460740982498013184/wIPwMwru'
        u'_normal.png')
    self.assertEqual(test_event.profile_image_url, expected_profile_image_url)
    self.assertEqual(test_event.profile_link_color_hex_triplet, 2052731)
    self.assertEqual(test_event.protected, 0)
    self.assertEqual(test_event.screen_name, u'BBCBreaking')
    self.assertEqual(test_event.statuses_count, 26697)
    self.assertIsNone(test_event.structured_location)
    self.assertEqual(test_event.url, u'http://www.bbc.co.uk/news')
    self.assertIsNone(test_event.url_entities)
    self.assertEqual(test_event.verified, 1)

    expected_message = (
        u'Screen Name: BBCBreaking Profile Image Url: https://pbs.twimg.co'
        u'm/profile_images/460740982498013184/wIPwMwru_normal.png Profile'
        u'Banner Url:'
        u'https://pbs.twimg.com/profile_banners/5402612/1398336837 Profile'
        u'Link Color Hex Triplet: 2052731 Location: London, UK Structured'
        u'Location: None Description: Breaking news alerts and updates'
        u'from the BBC. For news, features, analysis follow @BBCWorld'
        u'(international) or @BBCNews (UK). Latest sport news @BBCSport.'
        u'Url: http://www.bbc.co.uk/news Url Entities: None Bio Entities:'
        u'None Protected: 0 Verified: 1 Following: 0 Device Following: 0'
        u'Advertiser Account Type: 0 Statuses Count: 26697 Media Count:'
        u'None Favorites Count: 0 Following Count: 3 Followers Count:'
        u'19466932 Followers Count Fast: 0 Followers Count Normal: 0 Could'
        u'Be Stale: 0 Is Lifeline Institution: 0 Has Collections: 0 Is'
        u'Translator: 0 Has Extended Profile Fields: 0 Extended Profile'
        u'Fields: None Pinned Tweet Id: None Business Profile State: 0'
        u'Analytics Type: 0')
    expected_message_short = (
        u'Screen Name: BBCBreaking Profile Image Url:'
        u'https://pbs.twimg.com/profile_ima...')

    self._TestGetMessageStrings(
        test_event, expected_message, expected_message_short)

    # Test the first users name event.
    guessed_event = [
        e for e in storage_writer.events
        if e.advertiser_account_type == 0 and e.analytics_type == 0 and
        e.bio_entities == u'b&#39;{}&#39;' and e.business_profile_state == 0 and
        e.could_be_stale == 0 and e.description == u'How people build software'
        and e.device_following == 0 and e.extended_profile_fields is None and
        e.favorites_count == 155 and e.followers_count == 742086 and
        e.followers_count_fast == 0 and e.followers_count_normal == 742086 and
        e.following == 0 and e.following_count == 172 and
        e.has_collections == 0 and e.has_extended_profile_fields == 0 and
        e.is_lifeline_institution == 0 and e.is_translator == 0 and
        e.location == u'San Francisco, CA' and e.media_count == 33 and
        e.pinned_tweet_id is None and e.profile_banner_url ==
        u'https://pbs.twimg.com/profile_banners/13334762/1415719104' and
        e.profile_image_url ==
        u'https://pbs.twimg.com/profile_images/616309728688238592/pBeeJQDQ'
        u'_normal.png' and e.profile_link_color_hex_triplet == 255 and
        e.protected == 0 and e.screen_name == u'github' and
        e.statuses_count == 3120 and e.structured_location is None and
        e.url == u'https://t.co/FoKGHcCyJJ' and e.url_entities ==
        u'b&#39;{&#34;urls&#34;:[{&#34;url&#34;:&#34;https:\\/\\/t.co\\/Fo'
        u'KGHcCyJJ&#34;,&#34;rangeInDisplay.length&#34;:0,&#34;displayURL&'
        u'#34;:&#34;github.com&#34;,&#34;rangeInDisplay.location&#34;:0,&#'
        u'34;expandedURL&#34;:&#34;https:\\/\\/github.com&#34;,&#34;range.'
        u'location&#34;:0,&#34;range.length&#34;:23}]}&#39;' and e.verified == 1
    ][0]
    position = storage_writer.index(guessed_event)
    test_event = storage_writer.events[position]

    # TODO add expected formatted timestamp for timestamp in database: GitHub
    expected_timestamp = timelib.Timestamp.CopyFromString(u'TODO')
    self.assertEqual(test_event.timestamp, expected_timestamp)

    self.assertEqual(
        test_event.timestamp_desc, eventdata.EventTimestamp.CREATION_TIME)
    self.assertEqual(test_event.advertiser_account_type, 0)
    self.assertEqual(test_event.analytics_type, 0)
    self.assertEqual(test_event.bio_entities, u'b&#39;{}&#39;')
    self.assertEqual(test_event.business_profile_state, 0)
    self.assertEqual(test_event.could_be_stale, 0)
    self.assertEqual(test_event.description, u'How people build software')
    self.assertEqual(test_event.device_following, 0)
    self.assertIsNone(test_event.extended_profile_fields)
    self.assertEqual(test_event.favorites_count, 155)
    self.assertEqual(test_event.followers_count, 742086)
    self.assertEqual(test_event.followers_count_fast, 0)
    self.assertEqual(test_event.followers_count_normal, 742086)
    self.assertEqual(test_event.following, 0)
    self.assertEqual(test_event.following_count, 172)
    self.assertEqual(test_event.has_collections, 0)
    self.assertEqual(test_event.has_extended_profile_fields, 0)
    self.assertEqual(test_event.is_lifeline_institution, 0)
    self.assertEqual(test_event.is_translator, 0)
    self.assertEqual(test_event.location, u'San Francisco, CA')
    self.assertEqual(test_event.media_count, 33)
    self.assertIsNone(test_event.pinned_tweet_id)
    expected_profile_banner_url = (
        u'https://pbs.twimg.com/profile_banners/13334762/1415719104')
    self.assertEqual(test_event.profile_banner_url, expected_profile_banner_url)
    expected_profile_image_url = (
        u'https://pbs.twimg.com/profile_images/616309728688238592/pBeeJQDQ'
        u'_normal.png')
    self.assertEqual(test_event.profile_image_url, expected_profile_image_url)
    self.assertEqual(test_event.profile_link_color_hex_triplet, 255)
    self.assertEqual(test_event.protected, 0)
    self.assertEqual(test_event.screen_name, u'github')
    self.assertEqual(test_event.statuses_count, 3120)
    self.assertIsNone(test_event.structured_location)
    self.assertEqual(test_event.url, u'https://t.co/FoKGHcCyJJ')
    expected_url_entities = (
        u'b&#39;{&#34;urls&#34;:[{&#34;url&#34;:&#34;https:\\/\\/t.co\\/Fo'
        u'KGHcCyJJ&#34;,&#34;rangeInDisplay.length&#34;:0,&#34;displayURL&'
        u'#34;:&#34;github.com&#34;,&#34;rangeInDisplay.location&#34;:0,&#'
        u'34;expandedURL&#34;:&#34;https:\\/\\/github.com&#34;,&#34;range.'
        u'location&#34;:0,&#34;range.length&#34;:23}]}&#39;')
    self.assertEqual(test_event.url_entities, expected_url_entities)
    self.assertEqual(test_event.verified, 1)

    expected_message = (
        u'Screen Name: github Profile Image Url: https://pbs.twimg.com/pro'
        u'file_images/616309728688238592/pBeeJQDQ_normal.png Profile'
        u'Banner Url:'
        u'https://pbs.twimg.com/profile_banners/13334762/1415719104'
        u'Profile Link Color Hex Triplet: 255 Location: San Francisco, CA'
        u'Structured Location: None Description: How people build software'
        u'Url: https://t.co/FoKGHcCyJJ Url Entities: b&#39;{&#34;urls&#34;'
        u':[{&#34;url&#34;:&#34;https:\\/\\/t.co\\/FoKGHcCyJJ&#34;,&#34;ra'
        u'ngeInDisplay.length&#34;:0,&#34;displayURL&#34;:&#34;github.com&'
        u'#34;,&#34;rangeInDisplay.location&#34;:0,&#34;expandedURL&#34;:&'
        u'#34;https:\\/\\/github.com&#34;,&#34;range.location&#34;:0,&#34;'
        u'range.length&#34;:23}]}&#39; Bio Entities: b&#39;{}&#39;'
        u'Protected: 0 Verified: 1 Following: 0 Device Following: 0'
        u'Advertiser Account Type: 0 Statuses Count: 3120 Media Count: 33'
        u'Favorites Count: 155 Following Count: 172 Followers Count:'
        u'742086 Followers Count Fast: 0 Followers Count Normal: 742086'
        u'Could Be Stale: 0 Is Lifeline Institution: 0 Has Collections: 0'
        u'Is Translator: 0 Has Extended Profile Fields: 0 Extended Profile'
        u'Fields: None Pinned Tweet Id: None Business Profile State: 0'
        u'Analytics Type: 0')
    expected_message_short = (
        u'Screen Name: github Profile Image Url:'
        u'https://pbs.twimg.com/profile_images/6...')

    self._TestGetMessageStrings(
        test_event, expected_message, expected_message_short)

    # Test the first users updatedAt event.
    guessed_event = [
        e for e in storage_writer.events
        if e.advertiser_account_type == 0 and e.analytics_type == 0 and
        e.bio_entities ==
        u'b&#39;{&#34;urls&#34;:[{&#34;url&#34;:&#34;http:\\/\\/t.co\\/Ndc'
        u'gVZ9Un6&#34;,&#34;rangeInDisplay.length&#34;:0,&#34;displayURL&#'
        u'34;:&#34;tompohl.com\\/bio.png&#34;,&#34;rangeInDisplay.location'
        u'&#34;:0,&#34;expandedURL&#34;:&#34;http:\\/\\/tompohl.com\\/bio.'
        u'png&#34;,&#34;range.location&#34;:0,&#34;range.length&#34;:22}]}'
        u'&#39;' and e.business_profile_state == 0 and e.could_be_stale == 0 and
        e.description == u'http://t.co/NdcgVZ9Un6' and e.device_following == 0
        and e.extended_profile_fields is None and e.favorites_count == 267 and
        e.followers_count == 681 and e.followers_count_fast == 0 and
        e.followers_count_normal == 0 and e.following == 0 and
        e.following_count == 661 and e.has_collections == 0 and
        e.has_extended_profile_fields == 0 and e.is_lifeline_institution == 0
        and e.is_translator == 0 and e.location == u'Des Moines, Iowa' and
        e.media_count is None and e.pinned_tweet_id is None and
        e.profile_banner_url is None and e.profile_image_url ==
        u'https://pbs.twimg.com/profile_images/378800000102859706/83b823ec'
        u'53247f689a48d5d3bdeeeb16_normal.jpeg' and
        e.profile_link_color_hex_triplet == 33972 and e.protected == 0 and
        e.screen_name == u'tompohl' and e.statuses_count == 4922 and
        e.structured_location is None and e.url == u'http://t.co/FN9hFrj9Mm' and
        e.url_entities ==
        u'b&#39;{&#34;urls&#34;:[{&#34;url&#34;:&#34;http:\\/\\/t.co\\/FN9'
        u'hFrj9Mm&#34;,&#34;rangeInDisplay.length&#34;:0,&#34;displayURL&#'
        u'34;:&#34;tompohl.com&#34;,&#34;rangeInDisplay.location&#34;:0,&#'
        u'34;expandedURL&#34;:&#34;http:\\/\\/tompohl.com&#34;,&#34;range.'
        u'location&#34;:0,&#34;range.length&#34;:22}]}&#39;' and e.verified == 0
    ][0]
    position = storage_writer.index(guessed_event)
    test_event = storage_writer.events[position]

    # TODO add expected formatted timestamp for timestamp in database: 1449070777.562435
    expected_timestamp = timelib.Timestamp.CopyFromString(u'TODO')
    self.assertEqual(test_event.timestamp, expected_timestamp)

    self.assertEqual(
        test_event.timestamp_desc, eventdata.EventTimestamp.CREATION_TIME)
    self.assertEqual(test_event.advertiser_account_type, 0)
    self.assertEqual(test_event.analytics_type, 0)
    expected_bio_entities = (
        u'b&#39;{&#34;urls&#34;:[{&#34;url&#34;:&#34;http:\\/\\/t.co\\/Ndc'
        u'gVZ9Un6&#34;,&#34;rangeInDisplay.length&#34;:0,&#34;displayURL&#'
        u'34;:&#34;tompohl.com\\/bio.png&#34;,&#34;rangeInDisplay.location'
        u'&#34;:0,&#34;expandedURL&#34;:&#34;http:\\/\\/tompohl.com\\/bio.'
        u'png&#34;,&#34;range.location&#34;:0,&#34;range.length&#34;:22}]}'
        u'&#39;')
    self.assertEqual(test_event.bio_entities, expected_bio_entities)
    self.assertEqual(test_event.business_profile_state, 0)
    self.assertEqual(test_event.could_be_stale, 0)
    self.assertEqual(test_event.description, u'http://t.co/NdcgVZ9Un6')
    self.assertEqual(test_event.device_following, 0)
    self.assertIsNone(test_event.extended_profile_fields)
    self.assertEqual(test_event.favorites_count, 267)
    self.assertEqual(test_event.followers_count, 681)
    self.assertEqual(test_event.followers_count_fast, 0)
    self.assertEqual(test_event.followers_count_normal, 0)
    self.assertEqual(test_event.following, 0)
    self.assertEqual(test_event.following_count, 661)
    self.assertEqual(test_event.has_collections, 0)
    self.assertEqual(test_event.has_extended_profile_fields, 0)
    self.assertEqual(test_event.is_lifeline_institution, 0)
    self.assertEqual(test_event.is_translator, 0)
    self.assertEqual(test_event.location, u'Des Moines, Iowa')
    self.assertIsNone(test_event.media_count)
    self.assertIsNone(test_event.pinned_tweet_id)
    self.assertIsNone(test_event.profile_banner_url)
    expected_profile_image_url = (
        u'https://pbs.twimg.com/profile_images/378800000102859706/83b823ec'
        u'53247f689a48d5d3bdeeeb16_normal.jpeg')
    self.assertEqual(test_event.profile_image_url, expected_profile_image_url)
    self.assertEqual(test_event.profile_link_color_hex_triplet, 33972)
    self.assertEqual(test_event.protected, 0)
    self.assertEqual(test_event.screen_name, u'tompohl')
    self.assertEqual(test_event.statuses_count, 4922)
    self.assertIsNone(test_event.structured_location)
    self.assertEqual(test_event.url, u'http://t.co/FN9hFrj9Mm')
    expected_url_entities = (
        u'b&#39;{&#34;urls&#34;:[{&#34;url&#34;:&#34;http:\\/\\/t.co\\/FN9'
        u'hFrj9Mm&#34;,&#34;rangeInDisplay.length&#34;:0,&#34;displayURL&#'
        u'34;:&#34;tompohl.com&#34;,&#34;rangeInDisplay.location&#34;:0,&#'
        u'34;expandedURL&#34;:&#34;http:\\/\\/tompohl.com&#34;,&#34;range.'
        u'location&#34;:0,&#34;range.length&#34;:22}]}&#39;')
    self.assertEqual(test_event.url_entities, expected_url_entities)
    self.assertEqual(test_event.verified, 0)

    expected_message = (
        u'Screen Name: tompohl Profile Image Url: https://pbs.twimg.com/pr'
        u'ofile_images/378800000102859706/83b823ec53247f689a48d5d3bdeeeb16'
        u'_normal.jpeg Profile Banner Url: None Profile Link Color Hex'
        u'Triplet: 33972 Location: Des Moines, Iowa Structured Location:'
        u'None Description: http://t.co/NdcgVZ9Un6 Url:'
        u'http://t.co/FN9hFrj9Mm Url Entities: b&#39;{&#34;urls&#34;:[{&#3'
        u'4;url&#34;:&#34;http:\\/\\/t.co\\/FN9hFrj9Mm&#34;,&#34;rangeInDi'
        u'splay.length&#34;:0,&#34;displayURL&#34;:&#34;tompohl.com&#34;,&'
        u'#34;rangeInDisplay.location&#34;:0,&#34;expandedURL&#34;:&#34;ht'
        u'tp:\\/\\/tompohl.com&#34;,&#34;range.location&#34;:0,&#34;range.'
        u'length&#34;:22}]}&#39; Bio Entities: b&#39;{&#34;urls&#34;:[{&#3'
        u'4;url&#34;:&#34;http:\\/\\/t.co\\/NdcgVZ9Un6&#34;,&#34;rangeInDi'
        u'splay.length&#34;:0,&#34;displayURL&#34;:&#34;tompohl.com\\/bio.'
        u'png&#34;,&#34;rangeInDisplay.location&#34;:0,&#34;expandedURL&#3'
        u'4;:&#34;http:\\/\\/tompohl.com\\/bio.png&#34;,&#34;range.locatio'
        u'n&#34;:0,&#34;range.length&#34;:22}]}&#39; Protected: 0'
        u'Verified: 0 Following: 0 Device Following: 0 Advertiser Account'
        u'Type: 0 Statuses Count: 4922 Media Count: None Favorites Count:'
        u'267 Following Count: 661 Followers Count: 681 Followers Count'
        u'Fast: 0 Followers Count Normal: 0 Could Be Stale: 0 Is Lifeline'
        u'Institution: 0 Has Collections: 0 Is Translator: 0 Has Extended'
        u'Profile Fields: 0 Extended Profile Fields: None Pinned Tweet Id:'
        u'None Business Profile State: 0 Analytics Type: 0')
    expected_message_short = (
        u'Screen Name: tompohl Profile Image Url:'
        u'https://pbs.twimg.com/profile_images/...')

    self._TestGetMessageStrings(
        test_event, expected_message, expected_message_short)

    # Test the first users createdDate event.
    guessed_event = [
        e for e in storage_writer.events
        if e.advertiser_account_type == 0 and e.analytics_type == 0 and
        e.bio_entities == u'b&#39;{}&#39;' and e.business_profile_state == 0 and
        e.could_be_stale == 0 and e.description ==
        u'Director of @SenatorLeahy Center for Digital Investigation,'
        u'@Champlainedu Professor, Forensic Examiner - Vermont ICAC,'
        u'Marathoner, Bonsai enthusiast' and e.device_following == 0 and
        e.extended_profile_fields is None and e.favorites_count == 52 and
        e.followers_count == 1165 and e.followers_count_fast == 0 and
        e.followers_count_normal == 0 and e.following == 0 and e.following_count
        == 411 and e.has_collections == 0 and e.has_extended_profile_fields == 0
        and e.is_lifeline_institution == 0 and e.is_translator == 0 and
        e.location == u'Burlington, Vermont' and e.media_count is None and
        e.pinned_tweet_id is None and e.profile_banner_url ==
        u'https://pbs.twimg.com/profile_banners/15378399/1400611105' and
        e.profile_image_url ==
        u'https://pbs.twimg.com/profile_images/659825753/Rajewski_Pic_norm'
        u'al.jpg' and e.profile_link_color_hex_triplet == 39321 and
        e.protected == 0 and e.screen_name == u'jtrajewski' and
        e.statuses_count == 3096 and e.structured_location is None and
        e.url == u'http://t.co/GqYJCMnCeq' and e.url_entities ==
        u'b&#39;{&#34;urls&#34;:[{&#34;url&#34;:&#34;http:\\/\\/t.co\\/GqY'
        u'JCMnCeq&#34;,&#34;rangeInDisplay.length&#34;:0,&#34;displayURL&#'
        u'34;:&#34;jonrajewski.com\\/cyberblog&#34;,&#34;rangeInDisplay.lo'
        u'cation&#34;:0,&#34;expandedURL&#34;:&#34;http:\\/\\/jonrajewski.'
        u'com\\/cyberblog&#34;,&#34;range.location&#34;:0,&#34;range.lengt'
        u'h&#34;:22}]}&#39;' and e.verified == 0
    ][0]
    position = storage_writer.index(guessed_event)
    test_event = storage_writer.events[position]

    # TODO add expected formatted timestamp for timestamp in database: 1215702054.0
    expected_timestamp = timelib.Timestamp.CopyFromString(u'TODO')
    self.assertEqual(test_event.timestamp, expected_timestamp)

    self.assertEqual(
        test_event.timestamp_desc, eventdata.EventTimestamp.CREATION_TIME)
    self.assertEqual(test_event.advertiser_account_type, 0)
    self.assertEqual(test_event.analytics_type, 0)
    self.assertEqual(test_event.bio_entities, u'b&#39;{}&#39;')
    self.assertEqual(test_event.business_profile_state, 0)
    self.assertEqual(test_event.could_be_stale, 0)
    expected_description = (
        u'Director of @SenatorLeahy Center for Digital Investigation,'
        u'@Champlainedu Professor, Forensic Examiner - Vermont ICAC,'
        u'Marathoner, Bonsai enthusiast')
    self.assertEqual(test_event.description, expected_description)
    self.assertEqual(test_event.device_following, 0)
    self.assertIsNone(test_event.extended_profile_fields)
    self.assertEqual(test_event.favorites_count, 52)
    self.assertEqual(test_event.followers_count, 1165)
    self.assertEqual(test_event.followers_count_fast, 0)
    self.assertEqual(test_event.followers_count_normal, 0)
    self.assertEqual(test_event.following, 0)
    self.assertEqual(test_event.following_count, 411)
    self.assertEqual(test_event.has_collections, 0)
    self.assertEqual(test_event.has_extended_profile_fields, 0)
    self.assertEqual(test_event.is_lifeline_institution, 0)
    self.assertEqual(test_event.is_translator, 0)
    self.assertEqual(test_event.location, u'Burlington, Vermont')
    self.assertIsNone(test_event.media_count)
    self.assertIsNone(test_event.pinned_tweet_id)
    expected_profile_banner_url = (
        u'https://pbs.twimg.com/profile_banners/15378399/1400611105')
    self.assertEqual(test_event.profile_banner_url, expected_profile_banner_url)
    expected_profile_image_url = (
        u'https://pbs.twimg.com/profile_images/659825753/Rajewski_Pic_norm'
        u'al.jpg')
    self.assertEqual(test_event.profile_image_url, expected_profile_image_url)
    self.assertEqual(test_event.profile_link_color_hex_triplet, 39321)
    self.assertEqual(test_event.protected, 0)
    self.assertEqual(test_event.screen_name, u'jtrajewski')
    self.assertEqual(test_event.statuses_count, 3096)
    self.assertIsNone(test_event.structured_location)
    self.assertEqual(test_event.url, u'http://t.co/GqYJCMnCeq')
    expected_url_entities = (
        u'b&#39;{&#34;urls&#34;:[{&#34;url&#34;:&#34;http:\\/\\/t.co\\/GqY'
        u'JCMnCeq&#34;,&#34;rangeInDisplay.length&#34;:0,&#34;displayURL&#'
        u'34;:&#34;jonrajewski.com\\/cyberblog&#34;,&#34;rangeInDisplay.lo'
        u'cation&#34;:0,&#34;expandedURL&#34;:&#34;http:\\/\\/jonrajewski.'
        u'com\\/cyberblog&#34;,&#34;range.location&#34;:0,&#34;range.lengt'
        u'h&#34;:22}]}&#39;')
    self.assertEqual(test_event.url_entities, expected_url_entities)
    self.assertEqual(test_event.verified, 0)

    expected_message = (
        u'Screen Name: jtrajewski Profile Image Url: https://pbs.twimg.com'
        u'/profile_images/659825753/Rajewski_Pic_normal.jpg Profile Banner'
        u'Url: https://pbs.twimg.com/profile_banners/15378399/1400611105'
        u'Profile Link Color Hex Triplet: 39321 Location: Burlington,'
        u'Vermont Structured Location: None Description: Director of'
        u'@SenatorLeahy Center for Digital Investigation, @Champlainedu'
        u'Professor, Forensic Examiner - Vermont ICAC, Marathoner, Bonsai'
        u'enthusiast Url: http://t.co/GqYJCMnCeq Url Entities: b&#39;{&#34'
        u';urls&#34;:[{&#34;url&#34;:&#34;http:\\/\\/t.co\\/GqYJCMnCeq&#34'
        u';,&#34;rangeInDisplay.length&#34;:0,&#34;displayURL&#34;:&#34;jo'
        u'nrajewski.com\\/cyberblog&#34;,&#34;rangeInDisplay.location&#34;'
        u':0,&#34;expandedURL&#34;:&#34;http:\\/\\/jonrajewski.com\\/cyber'
        u'blog&#34;,&#34;range.location&#34;:0,&#34;range.length&#34;:22}]'
        u'}&#39; Bio Entities: b&#39;{}&#39; Protected: 0 Verified: 0'
        u'Following: 0 Device Following: 0 Advertiser Account Type: 0'
        u'Statuses Count: 3096 Media Count: None Favorites Count: 52'
        u'Following Count: 411 Followers Count: 1165 Followers Count Fast:'
        u'0 Followers Count Normal: 0 Could Be Stale: 0 Is Lifeline'
        u'Institution: 0 Has Collections: 0 Is Translator: 0 Has Extended'
        u'Profile Fields: 0 Extended Profile Fields: None Pinned Tweet Id:'
        u'None Business Profile State: 0 Analytics Type: 0')
    expected_message_short = (
        u'Screen Name: jtrajewski Profile Image Url:'
        u'https://pbs.twimg.com/profile_imag...')

    self._TestGetMessageStrings(
        test_event, expected_message, expected_message_short)


if __name__ == '__main__':
  unittest.main()
