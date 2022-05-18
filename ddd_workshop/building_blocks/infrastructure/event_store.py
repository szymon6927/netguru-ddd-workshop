from abc import ABC, abstractmethod
from dataclasses import asdict

from kink import inject
from pymongo.database import Database

from ddd_workshop.building_blocks.domain.domain_event import DomainEvent
from ddd_workshop.building_blocks.infrastructure.serialization import mongo_repo_serializer


class IEventStore(ABC):
    @abstractmethod
    def save(self, event: DomainEvent) -> None:
        ...


@inject
class MongoEventStore(IEventStore):
    def __init__(self, database: Database):
        self._collection = database["events"]

    def save(self, event: DomainEvent) -> None:
        event_data = asdict(event, dict_factory=mongo_repo_serializer)
        event_data.pop("_id")
        event_data.pop("name")
        event_data.pop("occurred_on")

        document = {
            "_id": event.id,
            "name": event.name,
            "occurred_on": event.occurred_on,
            "published": False,
            "data": event_data,
        }
        self._collection.insert_one(document)
