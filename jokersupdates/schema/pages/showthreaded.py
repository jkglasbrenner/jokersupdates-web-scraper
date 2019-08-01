from dataclasses import dataclass
from datetime import datetime as DateTime
from uuid import UUID

from jokersupdates.schema.base import BaseData


@dataclass
class ShowThreadedData(BaseData):
    post_id: UUID = None
    subject: str = None
    text: str = None
    posted_on: DateTime = None
    edited_on: DateTime = None

    @property
    def schema(self):
        return {
            "post_id": {"type": "uuid", "coerce": "uuid"},
            "subject": {"type": "string", "coerce": "string"},
            "text": {"type": "string", "coerce": "string", "nullable": True},
            "posted_on": {"type": "datetime", "coerce": "datetime"},
            "edited_on": {"type": "datetime", "coerce": "datetime", "nullable": True},
        }
