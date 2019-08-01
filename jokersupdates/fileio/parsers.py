import json
from typing import IO, Any, Callable, ClassVar, Dict

from .base import ParsedData, Parser

ConvertDataIO = Callable[[IO[Any]], ParsedData]
DataReadMode = Dict[str, ConvertDataIO]


def convert_dataio_to_string(file: IO[Any]) -> ParsedData:
    return file.read()


def convert_dataio_to_lines_list(file: IO[Any]) -> ParsedData:
    return file.readlines()


class DataParser(Parser):

    _read_mode: ClassVar[DataReadMode] = {
        "read": convert_dataio_to_string,
        "read_lines": convert_dataio_to_lines_list,
    }

    def __init__(self, read_mode: str = "read") -> None:

        try:
            self._read: ConvertDataIO = self._read_mode[read_mode]

        except AttributeError:
            raise AttributeError(f"{read_mode} is not a valid read mode.")

    def parse(self, file: IO[Any]) -> ParsedData:
        return self._read(file)


class JsonParser(Parser):
    def parse(self, file: IO[Any]) -> ParsedData:
        return json.load(file)
