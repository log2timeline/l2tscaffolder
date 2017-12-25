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

  SOURCE_LONG = u'Test Users'
  SOURCE_SHORT = u'Test'


class TestStatusesFormatter(interface.ConditionalEventFormatter):
  """test statuses event formatter."""

  DATA_TYPE = u'test:'
  """Correct Format String Pieces where needed"""

  FORMAT_STRING_PIECES = [
    u'Id:{id}',
    u'Text:{text}',
    u'User Id:{user_id}',
    u'In Reply To Status Id:{in_reply_to_status_id}',
    u'Retweeted Status Id:{retweeted_status_id}',
    u'Geotag:{geotag}',
    u'Entities:{entities}',
    u'Card:{card}',
    u'Card Users:{card_users}',
    u'Primary Card Type:{primary_card_type}',
    u'Card Version:{card_version}',
    u'Retweet Count:{retweet_count}',
    u'Favorite Count:{favorite_count}',
    u'Favorited:{favorited}',
    u'Extra Scribe Item:{extra_scribe_item}',
    u'Withheld Scope:{withheld_scope}',
    u'Withheld In Countries:{withheld_in_countries}',
    u'In Reply To Username:{in_reply_to_username}',
    u'Possibly Sensitive:{possibly_sensitive}',
    u'Is Possibly Sensitive Appealable:{is_possibly_sensitive_appealable}',
    u'Is Lifeline Alert:{is_lifeline_alert}',
    u'Is Truncated:{is_truncated}',
    u'Preview Length:{preview_length}',
    u'Full Text Length:{full_text_length}',
    u'Lang:{lang}',
    u'Supplmental Language:{supplmental_language}',
    u'Include In Profile Timeline:{include_in_profile_timeline}',
    u'Quoted Status Id:{quoted_status_id}',
    u'Source:{source}']

  #TODO: remove Format String Pieces for the short Format
  FORMAT_STRING_SHORT_PIECES = [
    u'Id:{id}',
    u'Text:{text}',
    u'User Id:{user_id}',
    u'In Reply To Status Id:{in_reply_to_status_id}',
    u'Retweeted Status Id:{retweeted_status_id}',
    u'Geotag:{geotag}',
    u'Entities:{entities}',
    u'Card:{card}',
    u'Card Users:{card_users}',
    u'Primary Card Type:{primary_card_type}',
    u'Card Version:{card_version}',
    u'Retweet Count:{retweet_count}',
    u'Favorite Count:{favorite_count}',
    u'Favorited:{favorited}',
    u'Extra Scribe Item:{extra_scribe_item}',
    u'Withheld Scope:{withheld_scope}',
    u'Withheld In Countries:{withheld_in_countries}',
    u'In Reply To Username:{in_reply_to_username}',
    u'Possibly Sensitive:{possibly_sensitive}',
    u'Is Possibly Sensitive Appealable:{is_possibly_sensitive_appealable}',
    u'Is Lifeline Alert:{is_lifeline_alert}',
    u'Is Truncated:{is_truncated}',
    u'Preview Length:{preview_length}',
    u'Full Text Length:{full_text_length}',
    u'Lang:{lang}',
    u'Supplmental Language:{supplmental_language}',
    u'Include In Profile Timeline:{include_in_profile_timeline}',
    u'Quoted Status Id:{quoted_status_id}',
    u'Source:{source}']

  SOURCE_LONG = u'Test Statuses'
  SOURCE_SHORT = u'Test'


manager.FormattersManager.RegisterFormatter(
    [TestUsersFormatter, TestStatusesFormatter])
