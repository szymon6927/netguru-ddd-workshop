from typing import Iterator

import pytest
from pymongo import MongoClient
from pymongo.database import Database


@pytest.fixture()
def mongodb() -> Iterator[Database]:
    mongo_client: MongoClient = MongoClient("mongodb://localhost:27017/")

    database = mongo_client.get_database("wallet")

    yield database

    mongo_client.drop_database("wallet")
