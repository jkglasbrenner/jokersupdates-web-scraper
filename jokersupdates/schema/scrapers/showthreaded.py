from dataclasses import dataclass, field
from typing import List

from jokersupdates.schema.base import BaseData
from jokersupdates.schema.pages import ShowThreadedData


@dataclass
class ShowThreadedScrapedData(BaseData):
    showthreaded: List[ShowThreadedData] = field(default_factory=list)

    @property
    def schema(self):
        return {
            "postlist": {
                "type": "list",
                "schema": {"type": "data", "schema": ShowThreadedData().schema},
            }
        }
