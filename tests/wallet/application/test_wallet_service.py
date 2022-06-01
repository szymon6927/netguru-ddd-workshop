import pytest
from bson.objectid import ObjectId
from pymongo.database import Database

from ddd_workshop.building_blocks.infrastructure.domain_event_publisher import StoreAndForwardDomainEventPublisher
from ddd_workshop.building_blocks.infrastructure.event_store import MongoEventStore
from ddd_workshop.wallet.application.dto import CreateWalletDTO, DecreaseBalanceDTO, IncreaseBalanceDTO
from ddd_workshop.wallet.application.wallet_service import WalletService
from ddd_workshop.wallet.domain.entities import Wallet
from ddd_workshop.wallet.domain.value_objects import Currency, Money
from ddd_workshop.wallet.infrastructure.repository import MongoWalletRepository


@pytest.fixture()
def wallet_service(new_mongodb: Database) -> WalletService:
    repo = MongoWalletRepository(new_mongodb)
    event_store = MongoEventStore(new_mongodb)
    event_publisher = StoreAndForwardDomainEventPublisher(event_store)
    service = WalletService(repo, event_publisher)
    return service


def test_can_create_wallet(new_mongodb: Database) -> None:
    # given
    repo = MongoWalletRepository(new_mongodb)
    event_store = MongoEventStore(new_mongodb)
    event_publisher = StoreAndForwardDomainEventPublisher(event_store)
    service = WalletService(repo, event_publisher)

    # when
    wallet = service.create_wallet(CreateWalletDTO(name="test wallet", owner=ObjectId(), currency="USD"))

    # then
    events = list(new_mongodb["events"].find({}))
    document = new_mongodb["wallet"].find_one({"_id": wallet.id})

    assert document["_id"] == wallet.id
    assert wallet._name == "test wallet"
    assert len(events) == 1


def test_can_increase_balance(wallet_service: WalletService, new_mongodb: Database) -> None:
    # when
    wallet = Wallet.create("test wallet", ObjectId(), currency=Currency.USD)
    new_mongodb["wallet"].insert_one(wallet.to_snapshot())

    # when
    wallet = wallet_service.increase_balance(IncreaseBalanceDTO(wallet_id=wallet.id, how_much=200, currency="USD"))

    # then
    document = new_mongodb["wallet"].find_one({"_id": wallet.id})
    assert document["balance"]["amount"] == 200
    assert document["balance"]["currency"] == "USD"
    assert wallet.balance == Money.of(200, "USD")


def test_can_decrease_balance(wallet_service: WalletService, new_mongodb: Database) -> None:
    # when
    wallet = Wallet.create("test wallet", ObjectId(), currency=Currency.USD)
    wallet.increase_balance(Money.of(300, "USD"))
    new_mongodb["wallet"].insert_one(wallet.to_snapshot())

    # when
    wallet = wallet_service.decrease_balance(DecreaseBalanceDTO(wallet_id=wallet.id, how_much=200, currency="USD"))

    # then
    document = new_mongodb["wallet"].find_one({"_id": wallet.id})
    assert document["balance"]["amount"] == 100
    assert document["balance"]["currency"] == "USD"
    assert wallet.balance == Money.of(100, "USD")
