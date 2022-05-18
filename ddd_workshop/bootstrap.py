from kink import di
from pymongo import MongoClient

from ddd_workshop.building_blocks.infrastructure.domain_event_publisher import (
    IDomainEventPublisher,
    StoreAndForwardDomainEventPublisher,
)
from ddd_workshop.building_blocks.infrastructure.event_store import MongoEventStore
from ddd_workshop.wallet.domain.repository import IWalletRepository
from ddd_workshop.wallet.infrastructure.repository import MongoWalletRepository


def bootstrap_di() -> None:
    mongo_client: MongoClient = MongoClient("mongodb://localhost:27017/ddd_workshop")
    mongo_database = mongo_client.get_database("ddd_workshop")

    di[IDomainEventPublisher] = StoreAndForwardDomainEventPublisher(MongoEventStore(mongo_database))
    di[IWalletRepository] = MongoWalletRepository(mongo_database)
