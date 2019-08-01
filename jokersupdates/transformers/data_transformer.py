from .base import Transformer


class DataTransformer(object):
    def __init__(self, transformer: Transformer) -> None:
        self._transformer: Transformer = transformer

    def transform(self, data):
        return self._transformer.transform(data)
