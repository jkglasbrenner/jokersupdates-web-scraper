from dataclasses import dataclass, field
from typing import List
from uuid import UUID

from jokersupdates.schema.base import BaseData


@dataclass
class RepliesTable(BaseData):
    parent_id: List[UUID] = field(default_factory=list)
    child_id: List[UUID] = field(default_factory=list)

    @property
    def schema(self):
        return {
            "parent_id": {"type": "list", "schema": {"type": "uuid"}},
            "child_id": {"type": "list", "schema": {"type": "uuid"}},
        }
