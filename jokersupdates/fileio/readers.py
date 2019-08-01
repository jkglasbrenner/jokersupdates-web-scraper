import bz2
import gzip
import io
import lzma
from os import PathLike as BasePathLike
from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, Callable, ClassVar, Dict

from .base import ParsedData, Parser

if TYPE_CHECKING:
    PathLike = BasePathLike[str]

else:
    PathLike = BasePathLike

OpenFile = Callable[..., IO[Any]]
FileReaders = Dict[str, OpenFile]


class DataReader(object):

    _file_readers: ClassVar[FileReaders] = {
        "bz2": bz2.open,
        "gz": gzip.open,
        "xz": lzma.open,
    }

    def __init__(self, parser: Parser) -> None:
        self._file_parser: Parser = parser

    def from_file(self, filename: PathLike) -> ParsedData:
        file_reader: str = Path(filename).suffix.lstrip(".")
        open_file: OpenFile = self._file_readers.get(file_reader, open)

        with open_file(filename, "rt") as f:
            parsed_data: ParsedData = self._file_parser.parse(f)

        return parsed_data

    def from_string(self, string: str) -> ParsedData:
        with io.StringIO(initial_value=string) as f:
            parsed_data: ParsedData = self._file_parser.parse(f)

        return parsed_data

    def from_binary(self, binary: bytes) -> ParsedData:
        with io.BytesIO(initial_bytes=binary) as f:
            parsed_data: ParsedData = self._file_parser.parse(f)

        return parsed_data

    def from_stream(self, stream: IO[Any]) -> ParsedData:
        parsed_data: ParsedData = self._file_parser.parse(stream)

        return parsed_data
