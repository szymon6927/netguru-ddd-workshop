from bson.objectid import ObjectId
from pymongo.database import Database

from ddd_workshop.building_blocks.custom_types import MongoDocument
from ddd_workshop.wallet.application.dto import CreateWalletDTO, DecreaseBalanceDTO, IncreaseBalanceDTO
from ddd_workshop.wallet.application.wallet_service import WalletService
from ddd_workshop.wallet.domain.value_objects import Money


def test_can_create_wallet(mongodb: Database, wallet_service: WalletService) -> None:
    # given
    dto = CreateWalletDTO(name="test wallet", owner=ObjectId(), currency="USD")

    # when
    wallet = wallet_service.create_wallet(dto)

    # then
    events = list(mongodb["events"].find({}))
    document = mongodb["wallet"].find_one({"_id": wallet.id})

    assert document["_id"] == wallet.id  # type: ignore
    assert len(events) == 1


def test_can_increase_balance(
    wallet_service: WalletService, mongodb: Database, wallet_raw_document: MongoDocument
) -> None:
    # given
    dto = IncreaseBalanceDTO(wallet_id=wallet_raw_document["_id"], how_much=200, currency="USD")
    mongodb["wallet"].insert_one(wallet_raw_document)

    # when
    wallet = wallet_service.increase_balance(dto)

    # then
    document = mongodb["wallet"].find_one({"_id": wallet.id})
    assert document["balance"]["amount"] == 300  # type: ignore
    assert document["balance"]["currency"] == "USD"  # type: ignore
    assert wallet.balance == Money.of(300, "USD")


def test_can_decrease_balance(
    wallet_service: WalletService, mongodb: Database, wallet_raw_document: MongoDocument
) -> None:
    # when
    mongodb["wallet"].insert_one(wallet_raw_document)
    dto = DecreaseBalanceDTO(wallet_id=wallet_raw_document["_id"], how_much=50, currency="USD")

    # when
    wallet = wallet_service.decrease_balance(dto)

    # then
    document = mongodb["wallet"].find_one({"_id": wallet.id})
    assert document["balance"]["amount"] == 50  # type: ignore
    assert document["balance"]["currency"] == "USD"  # type: ignore
    assert wallet.balance == Money.of(50, "USD")
