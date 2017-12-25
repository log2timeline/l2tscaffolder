# -*- coding: utf-8 -*-
"""the plugin database formatter."""

from plaso.formatters import interface
from plaso.formatters import manager
from plaso.lib import errors


class ThePluginUsersFormatter(interface.ConditionalEventFormatter):
  """the plugin users event formatter."""

  DATA_TYPE = u'the:plugin:'
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

  SOURCE_LONG = u'The Plugin Users'
  SOURCE_SHORT = u'The Plugin'

  #TODO: Add Mappings from value to description
  _ID = {}
  #TODO: Add Mappings from value to description
  _SCREEN_NAME = {}
  #TODO: Add Mappings from value to description
  _PROFILE_IMAGE_URL = {}

  def GetMessages(self, unused_formatter_mediator, event):
    """Determines the formatted message strings for an event object.

    Args:
      formatter_mediator (FormatterMediator): mediates the interactions between
          formatters and other components, such as storage and Windows EventLog
          resources.
      event (EventObject): event.

    Returns:
      tuple(str, str): formatted message string and short message string.

    Raises:
      WrongFormatter: if the event object cannot be formatted by the formatter.
    """
    if self.DATA_TYPE != event.data_type:
      raise errors.WrongFormatter(
          u'Unsupported data type: {0:s}.'.format(event.data_type))

    event_values = event.CopyToDict()

    id = event_values.get(u'id', None)
    if id is not None:
      event_values[u'id'] = (self._ID.get(id, u'UNKNOWN'))

    screen_name = event_values.get(u'screen_name', None)
    if screen_name is not None:
      event_values[u'screen_name'] = (
          self._SCREEN_NAME.get(screen_name, u'UNKNOWN'))

    profile_image_url = event_values.get(u'profile_image_url', None)
    if profile_image_url is not None:
      event_values[u'profile_image_url'] = (
          self._PROFILE_IMAGE_URL.get(profile_image_url, u'UNKNOWN'))

    return self._ConditionalFormatMessages(event_values)


class ThePluginStatusesFormatter(interface.ConditionalEventFormatter):
  """the plugin statuses event formatter."""

  DATA_TYPE = u'the:plugin:'
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

  SOURCE_LONG = u'The Plugin Statuses'
  SOURCE_SHORT = u'The Plugin'


manager.FormattersManager.RegisterFormatter(
    [ThePluginUsersFormatter, ThePluginStatusesFormatter])
