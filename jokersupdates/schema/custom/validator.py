import copy
from collections import Mapping, Sequence
from uuid import UUID

from cerberus import TypeDefinition, Validator

from jokersupdates.schema.base import BaseData
from jokersupdates.transformers import (
    DataTransformer,
    DateTimeNormalizer,
    FloatNormalizer,
    IndentWidthNormalizer,
    IntegerNormalizer,
    PostNumberNormalizer,
    StringNormalizer,
    UUIDNormalizer,
)


class CustomValidator(Validator):

    types_mapping = Validator.types_mapping.copy()
    types_mapping["data"] = TypeDefinition("data", (object,), ())
    types_mapping["uuid"] = TypeDefinition("uuid", (UUID,), ())
    _datetime_normalizer = DataTransformer(DateTimeNormalizer())
    _float_normalizer = DataTransformer(FloatNormalizer())
    _indent_width_normalizer = DataTransformer(IndentWidthNormalizer())
    _integer_normalizer = DataTransformer(IntegerNormalizer())
    _post_number_normalizer = DataTransformer(PostNumberNormalizer())
    _string_normalizer = DataTransformer(StringNormalizer())
    _uuid_normalizer = DataTransformer(UUIDNormalizer())

    def __init__(self, *args, **kwargs):
        kwargs["require_all"] = True
        super().__init__(*args, **kwargs)

    def _normalize_coerce_datetime(self, value):
        return self._datetime_normalizer.transform(value)

    def _normalize_coerce_float(self, value):
        return self._float_normalizer.transform(value)

    def _normalize_coerce_indent_width(self, value):
        return self._indent_width_normalizer.transform(value)

    def _normalize_coerce_integer(self, value):
        return self._integer_normalizer.transform(value)

    def _normalize_coerce_post_number(self, value):
        return self._post_number_normalizer.transform(value)

    def _normalize_coerce_string(self, value):
        return self._string_normalizer.transform(value)

    def _normalize_coerce_uuid(self, value):
        return self._uuid_normalizer.transform(value)

    def _validate_schema(self, schema, field, value):
        """{'type': ['dict', 'string'],
            'anyof': [
                {'check_with': 'schema'},
                {'check_with': 'bulk_schema'}
            ]
        }
        """
        if isinstance(value, (Sequence, Mapping)):
            super()._validate_schema(schema, field, value)

        elif isinstance(value, BaseData):
            validator = copy.copy(self)
            validator.validate(value.as_dict(), schema)

            if validator.errors:
                self._error(field, validator.errors)
