# -*- coding: utf-8 -*-
"""test plugin database formatter."""

from plaso.formatters import interface
from plaso.formatters import manager
from plaso.lib import errors


class TestPluginUsersFormatter(interface.ConditionalEventFormatter):
  """test plugin users event formatter."""

  DATA_TYPE = u'test:plugin:'
  """Correct Format String Pieces where needed"""

  FORMAT_STRING_PIECES = [
    u'Id:{id}',
    u'Screen Name:{screen_name}',
    u'Profile Image Url:{profile_image_url}',
    u'Profile Banner Url:{profile_banner_url}',
    u'Profile Link Color Hex Triplet:{profile_link_color_hex_triplet}',
    u'Name:{name}',
    u'Location:{location}',
    u'Structured Location:{structured_location}',
    u'Description:{description}',
    u'Url:{url}',
    u'Url Entities:{url_entities}',
    u'Bio Entities:{bio_entities}',
    u'Protected:{protected}',
    u'Verified:{verified}',
    u'Following:{following}',
    u'Device Following:{device_following}',
    u'Advertiser Account Type:{advertiser_account_type}',
    u'Statuses Count:{statuses_count}',
    u'Media Count:{media_count}',
    u'Favorites Count:{favorites_count}',
    u'Following Count:{following_count}',
    u'Followers Count:{followers_count}',
    u'Followers Count Fast:{followers_count_fast}',
    u'Followers Count Normal:{followers_count_normal}',
    u'Could Be Stale:{could_be_stale}',
    u'Is Lifeline Institution:{is_lifeline_institution}',
    u'Has Collections:{has_collections}',
    u'Is Translator:{is_translator}',
    u'Has Extended Profile Fields:{has_extended_profile_fields}',
    u'Extended Profile Fields:{extended_profile_fields}',
    u'Pinned Tweet Id:{pinned_tweet_id}',
    u'Business Profile State:{business_profile_state}',
    u'Analytics Type:{analytics_type}']

  #TODO: remove Format String Pieces for the short Format
  FORMAT_STRING_SHORT_PIECES = [
    u'Id:{id}',
    u'Screen Name:{screen_name}',
    u'Profile Image Url:{profile_image_url}',
    u'Profile Banner Url:{profile_banner_url}',
    u'Profile Link Color Hex Triplet:{profile_link_color_hex_triplet}',
    u'Name:{name}',
    u'Location:{location}',
    u'Structured Location:{structured_location}',
    u'Description:{description}',
    u'Url:{url}',
    u'Url Entities:{url_entities}',
    u'Bio Entities:{bio_entities}',
    u'Protected:{protected}',
    u'Verified:{verified}',
    u'Following:{following}',
    u'Device Following:{device_following}',
    u'Advertiser Account Type:{advertiser_account_type}',
    u'Statuses Count:{statuses_count}',
    u'Media Count:{media_count}',
    u'Favorites Count:{favorites_count}',
    u'Following Count:{following_count}',
    u'Followers Count:{followers_count}',
    u'Followers Count Fast:{followers_count_fast}',
    u'Followers Count Normal:{followers_count_normal}',
    u'Could Be Stale:{could_be_stale}',
    u'Is Lifeline Institution:{is_lifeline_institution}',
    u'Has Collections:{has_collections}',
    u'Is Translator:{is_translator}',
    u'Has Extended Profile Fields:{has_extended_profile_fields}',
    u'Extended Profile Fields:{extended_profile_fields}',
    u'Pinned Tweet Id:{pinned_tweet_id}',
    u'Business Profile State:{business_profile_state}',
    u'Analytics Type:{analytics_type}']

  SOURCE_LONG = u'Test Plugin Users'
  SOURCE_SHORT = u'Test Plugin'


manager.FormattersManager.RegisterFormatter([TestPluginUsersFormatter])
