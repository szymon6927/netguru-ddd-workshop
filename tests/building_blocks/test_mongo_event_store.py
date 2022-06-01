from pymongo.database import Database

from ddd_workshop.building_blocks.domain.domain_event import DomainEvent
from ddd_workshop.building_blocks.infrastructure.event_store import MongoEventStore


def test_can_save_event(fake_event: DomainEvent, new_mongodb: Database) -> None:
    # given
    mongo_event_store = MongoEventStore(new_mongodb)

    # when
    mongo_event_store.save(fake_event)

    # then
    result = list(new_mongodb["events"].find({}))
    assert len(result) == 1
    assert result[0]["name"] == "fake.event"
    assert result[0]["data"]["message"] == "test"
