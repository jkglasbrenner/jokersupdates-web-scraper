from dataclasses import dataclass
from datetime import datetime as DateTime
from uuid import UUID

from jokersupdates.schema.base import BaseData


@dataclass
class PostData(BaseData):
    post_id: UUID = None
    board: str = None
    number: int = None
    subject: str = None
    author: str = None
    views: int = None
    replies: int = None
    posted_on: DateTime = None
    indent_width: int = None

    @property
    def schema(self):
        return {
            "post_id": {"type": "uuid", "coerce": "uuid"},
            "board": {"type": "string", "coerce": "string"},
            "number": {"type": "integer", "coerce": "post_number"},
            "subject": {"type": "string", "coerce": "string"},
            "author": {"type": "string", "coerce": "string"},
            "views": {"type": "integer", "coerce": "integer", "nullable": True},
            "replies": {"type": "integer", "coerce": "integer", "nullable": True},
            "posted_on": {"type": "datetime", "coerce": "datetime", "nullable": True},
            "indent_width": {"type": "integer", "coerce": "indent_width"},
        }
