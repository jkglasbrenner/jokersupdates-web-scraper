import dataclasses
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseData(metaclass=ABCMeta):
    @property
    @abstractmethod
    def schema(self):
        pass

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)

    def as_dict(self):
        return dataclasses.asdict(self)
