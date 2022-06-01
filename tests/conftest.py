from datetime import datetime
from typing import Iterator

import pytest
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.database import Database

from ddd_workshop.building_blocks.custom_types import MongoDocument


@pytest.fixture()
def mongodb() -> Iterator[Database]:
    mongo_client: MongoClient = MongoClient("mongodb://localhost:27017/")

    database = mongo_client.get_database("wallet")

    yield database

    mongo_client.drop_database("wallet")


@pytest.fixture()
def wallet_raw_document() -> MongoDocument:
    return {
        "_id": ObjectId(),
        "name": "test wallet",
        "owner": ObjectId(),
        "balance": {
            "amount": 100,
            "currency": "USD",
        },
        "created_at": datetime.utcnow(),
    }
