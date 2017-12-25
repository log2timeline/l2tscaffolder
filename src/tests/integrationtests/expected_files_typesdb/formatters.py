# -*- coding: utf-8 -*-
"""the plugin database formatter."""

from plaso.formatters import interface
from plaso.formatters import manager
from plaso.lib import errors


class ThePluginBlobtypesFormatter(interface.ConditionalEventFormatter):
  """the plugin blobtypes event formatter."""

  DATA_TYPE = u'the:plugin:'
  """Correct Format String Pieces where needed"""

  FORMAT_STRING_PIECES = [
    u'Blobval:{blobval}']

  #TODO: remove Format String Pieces for the short Format
  FORMAT_STRING_SHORT_PIECES = [
    u'Blobval:{blobval}']

  SOURCE_LONG = u'The Plugin Blobtypes'
  SOURCE_SHORT = u'The Plugin'


class ThePluginIntegertypesFormatter(interface.ConditionalEventFormatter):
  """the plugin integertypes event formatter."""

  DATA_TYPE = u'the:plugin:'
  """Correct Format String Pieces where needed"""

  FORMAT_STRING_PIECES = [
    u'Intval:{intval}',
    u'Integerval:{integerval}',
    u'Tinyintval:{tinyintval}',
    u'Smallintval:{smallintval}',
    u'Mediumintval:{mediumintval}',
    u'Bigintval:{bigintval}',
    u'Unsignedbigintval:{unsignedbigintval}',
    u'Int2Val:{int2val}',
    u'Int8Val:{int8val}']

  #TODO: remove Format String Pieces for the short Format
  FORMAT_STRING_SHORT_PIECES = [
    u'Intval:{intval}',
    u'Integerval:{integerval}',
    u'Tinyintval:{tinyintval}',
    u'Smallintval:{smallintval}',
    u'Mediumintval:{mediumintval}',
    u'Bigintval:{bigintval}',
    u'Unsignedbigintval:{unsignedbigintval}',
    u'Int2Val:{int2val}',
    u'Int8Val:{int8val}']

  SOURCE_LONG = u'The Plugin Integertypes'
  SOURCE_SHORT = u'The Plugin'


class ThePluginNumerictypesFormatter(interface.ConditionalEventFormatter):
  """the plugin numerictypes event formatter."""

  DATA_TYPE = u'the:plugin:'
  """Correct Format String Pieces where needed"""

  FORMAT_STRING_PIECES = [
    u'Numericval:{numericval}',
    u'Decimalval:{decimalval}',
    u'Booleanval:{booleanval}',
    u'Dateval:{dateval}',
    u'Datetimeval:{datetimeval}']

  #TODO: remove Format String Pieces for the short Format
  FORMAT_STRING_SHORT_PIECES = [
    u'Numericval:{numericval}',
    u'Decimalval:{decimalval}',
    u'Booleanval:{booleanval}',
    u'Dateval:{dateval}',
    u'Datetimeval:{datetimeval}']

  SOURCE_LONG = u'The Plugin Numerictypes'
  SOURCE_SHORT = u'The Plugin'


class ThePluginRealtypesFormatter(interface.ConditionalEventFormatter):
  """the plugin realtypes event formatter."""

  DATA_TYPE = u'the:plugin:'
  """Correct Format String Pieces where needed"""

  FORMAT_STRING_PIECES = [
    u'Realval:{realval}',
    u'Doubleval:{doubleval}',
    u'Doubleprecesionval:{doubleprecesionval}',
    u'Floatval:{floatval}']

  #TODO: remove Format String Pieces for the short Format
  FORMAT_STRING_SHORT_PIECES = [
    u'Realval:{realval}',
    u'Doubleval:{doubleval}',
    u'Doubleprecesionval:{doubleprecesionval}',
    u'Floatval:{floatval}']

  SOURCE_LONG = u'The Plugin Realtypes'
  SOURCE_SHORT = u'The Plugin'


class ThePluginTexttypesFormatter(interface.ConditionalEventFormatter):
  """the plugin texttypes event formatter."""

  DATA_TYPE = u'the:plugin:'
  """Correct Format String Pieces where needed"""

  FORMAT_STRING_PIECES = [
    u'Characterval:{characterval}',
    u'Varcharval:{varcharval}',
    u'Varyingcharacterval:{varyingcharacterval}',
    u'Ncharval:{ncharval}',
    u'Nativecharacterval:{nativecharacterval}',
    u'Nvarchar Val:{nvarchar_val}',
    u'Textval:{textval}',
    u'Clobval:{clobval}']

  #TODO: remove Format String Pieces for the short Format
  FORMAT_STRING_SHORT_PIECES = [
    u'Characterval:{characterval}',
    u'Varcharval:{varcharval}',
    u'Varyingcharacterval:{varyingcharacterval}',
    u'Ncharval:{ncharval}',
    u'Nativecharacterval:{nativecharacterval}',
    u'Nvarchar Val:{nvarchar_val}',
    u'Textval:{textval}',
    u'Clobval:{clobval}']

  SOURCE_LONG = u'The Plugin Texttypes'
  SOURCE_SHORT = u'The Plugin'


class ThePluginNodataFormatter(interface.ConditionalEventFormatter):
  """the plugin nodata event formatter."""

  DATA_TYPE = u'the:plugin:'
  """Correct Format String Pieces where needed"""

  FORMAT_STRING_PIECES = [
    u'Intval:{intval}',
    u'Integerval:{integerval}',
    u'Tinyintval:{tinyintval}',
    u'Smallintval:{smallintval}',
    u'Mediuintval:{mediuintval}',
    u'Bigintval:{bigintval}',
    u'Unsignedbigintval:{unsignedbigintval}',
    u'Int2Val:{int2val}',
    u'Int8Val:{int8val}',
    u'Characterval:{characterval}',
    u'Varcharval:{varcharval}',
    u'Varyingcharacterval:{varyingcharacterval}',
    u'Ncharval:{ncharval}',
    u'Nativecharacterval:{nativecharacterval}',
    u'Nvarcharval:{nvarcharval}',
    u'Textval:{textval}',
    u'Clobval:{clobval}',
    u'Blobval:{blobval}',
    u'Realval:{realval}',
    u'Doubleval:{doubleval}',
    u'Doubleprecisionval:{doubleprecisionval}',
    u'Floatval:{floatval}',
    u'Numericval:{numericval}',
    u'Decimalval:{decimalval}',
    u'Booleanval:{booleanval}',
    u'Dateval:{dateval}',
    u'Datetimeval:{datetimeval}']

  #TODO: remove Format String Pieces for the short Format
  FORMAT_STRING_SHORT_PIECES = [
    u'Intval:{intval}',
    u'Integerval:{integerval}',
    u'Tinyintval:{tinyintval}',
    u'Smallintval:{smallintval}',
    u'Mediuintval:{mediuintval}',
    u'Bigintval:{bigintval}',
    u'Unsignedbigintval:{unsignedbigintval}',
    u'Int2Val:{int2val}',
    u'Int8Val:{int8val}',
    u'Characterval:{characterval}',
    u'Varcharval:{varcharval}',
    u'Varyingcharacterval:{varyingcharacterval}',
    u'Ncharval:{ncharval}',
    u'Nativecharacterval:{nativecharacterval}',
    u'Nvarcharval:{nvarcharval}',
    u'Textval:{textval}',
    u'Clobval:{clobval}',
    u'Blobval:{blobval}',
    u'Realval:{realval}',
    u'Doubleval:{doubleval}',
    u'Doubleprecisionval:{doubleprecisionval}',
    u'Floatval:{floatval}',
    u'Numericval:{numericval}',
    u'Decimalval:{decimalval}',
    u'Booleanval:{booleanval}',
    u'Dateval:{dateval}',
    u'Datetimeval:{datetimeval}']

  SOURCE_LONG = u'The Plugin Nodata'
  SOURCE_SHORT = u'The Plugin'


manager.FormattersManager.RegisterFormatter([
    ThePluginBlobtypesFormatter, ThePluginIntegertypesFormatter,
    ThePluginNumerictypesFormatter, ThePluginRealtypesFormatter,
    ThePluginTexttypesFormatter, ThePluginNodataFormatter
])
