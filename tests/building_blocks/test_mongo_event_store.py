from pymongo.database import Database

from ddd_workshop.building_blocks.domain.domain_event import DomainEvent
from ddd_workshop.building_blocks.infrastructure.event_store import MongoEventStore


def test_can_save_event(workshop_started_test_event: DomainEvent, mongodb: Database) -> None:
    # given
    mongo_event_store = MongoEventStore(mongodb)

    # when
    mongo_event_store.save(workshop_started_test_event)

    # then
    result = list(mongodb["events"].find({}))
    assert len(result) == 1
    assert result[0]["name"] == "workshop.started"
    assert result[0]["data"]["message"] == "Welcome everyone!"
