import json
from datetime import datetime as DateTime
from functools import singledispatch
from typing import IO, Any

from .base import JsonSerializableData, Serializer


class TextSerializer(Serializer):
    @property
    def mode(self) -> str:
        return "wt"

    def write(self, obj: str, file: IO[Any]) -> None:
        file.write(obj)


class BinarySerializer(Serializer):
    @property
    def mode(self) -> str:
        return "wb"

    def write(self, obj: bytes, file: IO[Any]) -> None:
        file.write(obj)


class JsonSerializer(Serializer):
    @property
    def mode(self) -> str:
        return "wt"

    def write(self, obj: JsonSerializableData, file: IO[Any]) -> None:
        json.dump(obj=obj, fp=file, default=self._to_serializable)

    @staticmethod
    @singledispatch
    def _to_serializable(value) -> str:
        return str(value)

    @staticmethod
    @_to_serializable.register(DateTime)
    def _serialize_datetime(value) -> str:
        return str(value.isoformat())
