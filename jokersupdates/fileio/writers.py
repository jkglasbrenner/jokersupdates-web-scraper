import bz2
import gzip
import lzma
from os import PathLike as BasePathLike
from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, Callable, ClassVar, Dict

from .base import SerializableData, Serializer

if TYPE_CHECKING:
    PathLike = BasePathLike[str]

else:
    PathLike = BasePathLike

OpenFile = Callable[..., IO[Any]]
FileWriters = Dict[str, OpenFile]


class DataWriter(object):

    _file_writers: ClassVar[FileWriters] = {
        "bz2": bz2.open,
        "gz": gzip.open,
        "xz": lzma.open,
    }

    def __init__(self, writer: Serializer) -> None:
        self._file_writer: Serializer = writer

    def to_file(self, obj: SerializableData, filename: PathLike) -> None:
        file_writer: str = Path(filename).suffix.lstrip(".")

        if self._file_writer.mode == "wb" and file_writer == "zip":
            open_file: OpenFile = open

        else:
            open_file = self._file_writers.get(file_writer, open)

        with open_file(filename, self._file_writer.mode) as f:
            self._file_writer.write(obj, f)
