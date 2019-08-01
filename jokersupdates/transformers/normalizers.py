import re
from datetime import datetime as DateTime
from uuid import UUID

import pytz

from .base import Transformer


class DateTimeNormalizer(Transformer):

    board_timezone = pytz.timezone("America/Los_Angeles")
    posted_on_format = "%m/%d/%y %I:%M %p"
    edited_on_format = "Edited (%m/%d/%y %I:%M %p)"

    def transform(self, data):
        if isinstance(data, DateTime):
            return data

        return self._parse_data(data)

    def _parse_data(self, data):
        date_string_formats = (self.posted_on_format, self.edited_on_format)

        for format in date_string_formats:
            try:
                return self._parse_formatted_datetime(data, format, self.board_timezone)

            except ValueError:
                pass

        try:
            return self._parse_isoformat_datetime(data)

        except ValueError:
            pass

        return None

    @staticmethod
    def _parse_formatted_datetime(date_string, format, timezone):
        datetime_no_tz = DateTime.strptime(date_string, format)
        datetime_local_tz = timezone.localize(datetime_no_tz)
        datetime_utc_tz = datetime_local_tz.astimezone(pytz.utc)

        return datetime_utc_tz

    @staticmethod
    def _parse_isoformat_datetime(date_string):
        return DateTime.fromisoformat(date_string)


class FloatNormalizer(Transformer):
    def __init__(self, default=None):
        self._default = default

    def transform(self, data):
        if data is not None:
            return self._parse_data(data)

        return self._default

    def _parse_data(self, data):
        try:
            return float(data)

        except ValueError:
            pass

        return self._default


class IndentWidthNormalizer(Transformer):
    def transform(self, data):
        if isinstance(data, int):
            return data

        return self._parse_data(data)

    def _parse_data(self, data):
        try:
            return self._parse_indent_width(data)

        except AttributeError:
            pass

        return 0

    @staticmethod
    def _parse_indent_width(data):
        indent_width = data.get("width")

        return int(indent_width)


class IntegerNormalizer(Transformer):
    def __init__(self, default=None):
        self._default = default

    def transform(self, data):
        if data is not None:
            return self._parse_data(data)

        return self._default

    def _parse_data(self, data):
        try:
            return int(data)

        except ValueError:
            pass

        return self._default


class PostNumberNormalizer(Transformer):

    digits_regex = re.compile(r"\d+")

    def transform(self, data):
        if isinstance(data, int):
            return data

        return self._parse_data(data)

    def _parse_data(self, data):
        try:
            return self._parse_postrow_id(data, self.digits_regex)

        except ValueError:
            pass

        try:
            return int(data)

        except ValueError:
            pass

        return None

    @staticmethod
    def _parse_postrow_id(data, regex):
        number_list = regex.findall(data)

        return int(number_list[0])


class StringNormalizer(Transformer):
    def transform(self, data):
        if not data.strip():
            return None

        return self._parse_data(data)

    def _parse_data(self, data):
        try:
            return str(data)

        except ValueError:
            pass

        return None


class UUIDNormalizer(Transformer):
    def transform(self, data):
        if isinstance(data, UUID):
            return data

        return self._parse_data(data)

    def _parse_data(self, data):
        parsers = (
            (self._parse_uuid_hex, (AttributeError, TypeError, ValueError)),
            (self._parse_uuid_bytes, (TypeError, ValueError)),
            (self._parse_uuid_bytes_le, (TypeError, ValueError)),
            (self._parse_uuid_fields, (TypeError, ValueError)),
            (self._parse_uuid_int, (TypeError,)),
        )

        for parse, errors in parsers:
            try:
                return parse(data)

            except errors:
                pass

        return None

    @staticmethod
    def _parse_uuid_hex(data):
        return UUID(hex=data)

    @staticmethod
    def _parse_uuid_bytes(data):
        return UUID(bytes=data)

    @staticmethod
    def _parse_uuid_bytes_le(data):
        return UUID(bytes_le=data)

    @staticmethod
    def _parse_uuid_fields(data):
        return UUID(fields=data)

    @staticmethod
    def _parse_uuid_int(data):
        return UUID(int=data)
