import pytest
from bson import ObjectId
from pymongo.database import Database

from ddd_workshop.building_blocks.custom_types import MongoDocument
from ddd_workshop.wallet.domain.entities import Wallet
from ddd_workshop.wallet.domain.errors import WalletNotFound
from ddd_workshop.wallet.domain.value_objects import Currency, Money
from ddd_workshop.wallet.infrastructure.repository import MongoWalletRepository


def test_can_save_wallet(mongodb: Database) -> None:
    # given
    wallet = Wallet.create(name="test", owner=ObjectId(), currency=Currency.USD)
    repo = MongoWalletRepository(mongodb)

    # when
    repo.save(wallet)

    # then
    document = mongodb["wallet"].find_one({"_id": wallet.id})
    assert document["_id"] == wallet.id  # type: ignore


def test_can_get_wallet(mongodb: Database, wallet_raw_document: MongoDocument) -> None:
    # given
    mongodb["wallet"].insert_one(wallet_raw_document)
    repo = MongoWalletRepository(mongodb)

    # when
    wallet = repo.get(wallet_raw_document["_id"])

    # then
    assert wallet.id == wallet_raw_document["_id"]
    assert wallet.balance == Money.of(
        wallet_raw_document["balance"]["amount"],
        wallet_raw_document["balance"]["currency"],
    )


def test_should_raise_an_exception_if_wallet_not_in_db(mongodb: Database) -> None:
    # given
    repo = MongoWalletRepository(mongodb)

    # expect
    with pytest.raises(WalletNotFound):
        repo.get(ObjectId())
