import pytest
from bson import ObjectId
from pymongo.database import Database

from ddd_workshop.wallet.domain.entities import Wallet
from ddd_workshop.wallet.domain.errors import WalletNotFound
from ddd_workshop.wallet.domain.value_objects import Currency
from ddd_workshop.wallet.infrastructure.repository import MongoWalletRepository


def test_can_save_wallet(new_mongodb: Database) -> None:
    # given
    wallet = Wallet.create(name="test", owner=ObjectId(), currency=Currency.USD)
    repo = MongoWalletRepository(new_mongodb)

    # when
    repo.save(wallet)

    # then
    document = new_mongodb["wallet"].find_one({"_id": wallet.id})
    assert document["_id"] == wallet.id  # type: ignore


def test_can_get_wallet(new_mongodb: Database) -> None:
    # given
    wallet_old = Wallet.create(name="test", owner=ObjectId(), currency=Currency.USD)
    new_mongodb["wallet"].insert_one(wallet_old.to_snapshot())
    repo = MongoWalletRepository(new_mongodb)

    # when
    wallet_new = repo.get(wallet_old.id)

    # then
    assert wallet_old.id == wallet_new.id
    assert wallet_old.balance == wallet_new.balance


def test_should_raise_an_exception_if_wallet_not_in_db(new_mongodb: Database) -> None:
    # given
    wallet = Wallet.create(name="test", owner=ObjectId(), currency=Currency.USD)
    repo = MongoWalletRepository(new_mongodb)

    # expect
    with pytest.raises(WalletNotFound):
        repo.get(wallet.id)
