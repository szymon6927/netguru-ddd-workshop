from dataclasses import dataclass
from datetime import datetime

import pytest
from bson.objectid import ObjectId

from ddd_workshop.building_blocks.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class WorkshopStarted(DomainEvent):
    message: str


@pytest.fixture()
def workshop_started_test_event() -> DomainEvent:
    return WorkshopStarted(
        id=ObjectId(),
        name="workshop.started",
        occurred_on=datetime.utcnow(),
        message="Welcome everyone!",
    )
