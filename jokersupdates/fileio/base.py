from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Union

JsonData = Dict[Any, str]
JsonSerializableData = Dict[Any, Any]
ParsedData = Union[str, bytes, List[str], JsonData]
SerializableData = Union[str, bytes, JsonSerializableData]


class Parser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, file) -> ParsedData:
        pass


class Serializer(metaclass=ABCMeta):
    @property
    @abstractmethod
    def mode(self) -> str:
        pass

    @abstractmethod
    def write(self, obj, file) -> None:
        pass
