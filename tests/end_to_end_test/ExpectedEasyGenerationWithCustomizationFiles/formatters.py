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

  #TODO: Add Mappings from value to description
  _LOCATION = {}

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

    location = event_values.get(u'location', None)
    if location is not None:
      event_values[u'location'] = (self._LOCATION.get(location, u'UNKNOWN'))

    return self._ConditionalFormatMessages(event_values)


manager.FormattersManager.RegisterFormatter([TestUsersFormatter])
