from typing import Any, Dict, Optional

from jokersupdates.schema.base import BaseData

from .errors import DataValidationError
from .validator import CustomValidator

Parameters = Dict[Any, Any]


class DataValidator(object):

    validator = CustomValidator()

    def __init__(self, data: Optional[BaseData] = None):
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, BaseData):
            self._data: BaseData = value

        elif value is None:
            self._data = None

    @property
    def errors(self):
        if not self.valid:
            return self.validator.errors

        return None

    @property
    def valid(self):
        return self.validator.validate(self.data.as_dict(), self.data.schema)

    def normalize(self, data: Optional[BaseData] = None, strict: bool = False):
        if data is not None:
            self.data = data

        valid: bool = self.valid

        if strict and not valid:
            raise DataValidationError(
                "Data has validation errors and cannot be normalized."
            )

        normalized_data: CustomValidator = self.validator.document

        return self.data.from_dict(normalized_data)

    def validate(self, data: Optional[BaseData] = None):
        if data is not None:
            self.data = data

        return self.valid
