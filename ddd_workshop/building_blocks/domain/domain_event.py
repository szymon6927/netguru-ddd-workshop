from dataclasses import dataclass
from datetime import datetime

from bson.objectid import ObjectId


@dataclass(frozen=True)
class DomainEvent:
    id: ObjectId
    name: str
    occurred_on: datetime
