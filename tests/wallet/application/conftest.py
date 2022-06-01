from datetime import datetime
from typing import List

import pytest
from bson.objectid import ObjectId
from pymongo.database import Database

from ddd_workshop.building_blocks.custom_types import MongoDocument
from ddd_workshop.building_blocks.infrastructure.domain_event_publisher import StoreAndForwardDomainEventPublisher
from ddd_workshop.building_blocks.infrastructure.event_store import MongoEventStore
from ddd_workshop.wallet.application.wallet_service import WalletService
from ddd_workshop.wallet.infrastructure.repository import MongoWalletRepository


@pytest.fixture()
def wallet_service(mongodb: Database) -> WalletService:
    repo = MongoWalletRepository(mongodb)
    event_store = MongoEventStore(mongodb)
    event_publisher = StoreAndForwardDomainEventPublisher(event_store)
    service = WalletService(repo, event_publisher)
    return service


@pytest.fixture()
def example_wallet_id() -> ObjectId:
    return ObjectId()


@pytest.fixture()
def transaction_events(example_wallet_id: ObjectId) -> List[MongoDocument]:
    events = [
        {
            "_id": ObjectId(),
            "name": "wallet.balance.increased",
            "occurred_on": datetime.utcnow(),
            "data": {
                "wallet_id": example_wallet_id,
                "how_much": 100,
                "currency": "GBP",
            },
        },
        {
            "_id": ObjectId(),
            "name": "wallet.balance.increased",
            "occurred_on": datetime.utcnow(),
            "data": {
                "wallet_id": example_wallet_id,
                "how_much": 100,
                "currency": "GBP",
            },
        },
        {
            "_id": ObjectId(),
            "name": "wallet.balance.decreased",
            "occurred_on": datetime.utcnow(),
            "data": {"wallet_id": example_wallet_id, "how_much": 50, "currency": "GBP"},
        },
    ]
    return events


@pytest.fixture()
def example_wallets_owner() -> ObjectId:
    return ObjectId()


@pytest.fixture()
def wallets_with_owner(example_wallets_owner: ObjectId) -> List[MongoDocument]:
    return [
        {
            "_id": ObjectId(),
            "name": "test wallet 1",
            "owner": example_wallets_owner,
            "balance": {
                "amount": 100,
                "currency": "USD",
            },
            "created_at": datetime.utcnow(),
        },
        {
            "_id": ObjectId(),
            "name": "test wallet 2",
            "owner": example_wallets_owner,
            "balance": {
                "amount": 256,
                "currency": "GBP",
            },
            "created_at": datetime.utcnow(),
        },
        {
            "_id": ObjectId(),
            "name": "test wallet 3",
            "owner": example_wallets_owner,
            "balance": {
                "amount": 512,
                "currency": "EUR",
            },
            "created_at": datetime.utcnow(),
        },
    ]
