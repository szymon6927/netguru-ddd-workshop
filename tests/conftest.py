from dataclasses import dataclass
from datetime import datetime
from typing import Iterator

import pytest
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.database import Database

from ddd_workshop.building_blocks.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class FakeEvent(DomainEvent):
    message: str


@pytest.fixture()
def new_mongodb() -> Iterator[Database]:
    mongo_client: MongoClient = MongoClient("mongodb://localhost:27017/")

    database = mongo_client.get_database("wallet")

    yield database

    mongo_client.drop_database("wallet")


@pytest.fixture()
def fake_event() -> DomainEvent:
    return FakeEvent(id=ObjectId(), name="fake.event", occurred_on=datetime.utcnow(), message="test")
