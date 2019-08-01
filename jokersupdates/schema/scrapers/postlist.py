from dataclasses import dataclass, field
from typing import List

from jokersupdates.schema.base import BaseData
from jokersupdates.schema.pages import PostData


@dataclass
class PostListScrapedData(BaseData):
    postlist: List[PostData] = field(default_factory=list)

    @property
    def schema(self):
        return {
            "postlist": {
                "type": "list",
                "schema": {"type": "data", "schema": PostData().schema},
            }
        }
