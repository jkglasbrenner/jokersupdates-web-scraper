from abc import ABCMeta, abstractmethod


class Transformer(metaclass=ABCMeta):
    @abstractmethod
    def transform(self, data):
        pass
