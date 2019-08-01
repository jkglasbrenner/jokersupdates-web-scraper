import uuid
from urllib.parse import urlencode, urlunsplit

from .base import Transformer


class UrlBuilder(Transformer):
    def __init__(self, baseurl_tuple, board):
        self._baseurl_tuple = baseurl_tuple
        self._board = board

    def transform(self, data):
        parameters = {"Board": self._board}

        if data:
            parameters["Number"] = data

        return urlunsplit(self._baseurl_tuple + (urlencode(parameters), ""))


class UUIDBuilder(Transformer):
    def __init__(self, namespace):
        self._namespace = namespace

    def transform(self, data):
        return uuid.uuid3(self._namespace, data)
