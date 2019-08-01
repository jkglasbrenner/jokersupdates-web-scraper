from dataclasses import dataclass, field
from datetime import datetime as DateTime
from typing import List
from uuid import UUID

from jokersupdates.schema.base import BaseData


@dataclass
class PostsTable(BaseData):
    post_id: List[UUID] = field(default_factory=list)
    board: List[str] = field(default_factory=list)
    number: List[int] = field(default_factory=list)
    subject: List[str] = field(default_factory=list)
    author: List[str] = field(default_factory=list)
    views: List[int] = field(default_factory=list)
    replies: List[int] = field(default_factory=list)
    posted_on: List[DateTime] = field(default_factory=list)
    edited_on: List[DateTime] = field(default_factory=list)
    text: List[str] = field(default_factory=list)

    @property
    def schema(self):
        return {
            "post_id": {"type": "list", "schema": {"type": "uuid"}},
            "board": {"type": "list", "schema": {"type": "string"}},
            "number": {"type": "list", "schema": {"type": "integer"}},
            "subject": {"type": "list", "schema": {"type": "string"}},
            "author": {"type": "list", "schema": {"type": "string"}},
            "views": {"type": "list", "schema": {"type": "integer", "nullable": True}},
            "replies": {
                "type": "list",
                "schema": {"type": "integer", "nullable": True},
            },
            "posted_on": {"type": "list", "schema": {"type": "datetime"}},
            "edited_on": {
                "type": "list",
                "schema": {"type": "datetime", "nullable": True},
            },
            "text": {"type": "list", "schema": {"type": "string", "nullable": True}},
        }
