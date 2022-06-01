from typing import List

from bson.objectid import ObjectId
from pymongo.database import Database

from ddd_workshop.building_blocks.custom_types import MongoDocument
from ddd_workshop.wallet.application.query import TransactionsHistory
from ddd_workshop.wallet.application.query_handler import QueryHandler


def test_can_get_transactions_history(
    mongodb: Database,
    transaction_events: List[MongoDocument],
    example_wallet_id: ObjectId,
) -> None:
    # given
    mongodb["events"].insert_many(transaction_events)
    query_handler = QueryHandler(mongodb)

    # when
    result = query_handler.get_transactions_history(TransactionsHistory(wallet_id=example_wallet_id))

    # then
    assert len(result) == 3
    assert result[0].amount == 100
    assert result[0].type == "+"
    assert result[1].amount == 100
    assert result[1].type == "+"
    assert result[2].amount == 50
    assert result[2].type == "-"


def test_should_return_empty_list_if_no_transactions_for_a_wallet(
    mongodb: Database, example_wallet_id: ObjectId
) -> None:
    # given
    query_handler = QueryHandler(mongodb)

    # when
    result = query_handler.get_transactions_history(TransactionsHistory(wallet_id=example_wallet_id))

    # then
    assert len(result) == 0


def test_can_get_all_wallets_assigned_to_owner(
    mongodb: Database,
    wallets_with_owner: List[MongoDocument],
    example_wallets_owner: ObjectId,
) -> None:
    # given
    mongodb["wallets"].insert_many(wallets_with_owner)
    query_handler = QueryHandler(mongodb)

    # when
    result = query_handler.get_all_wallets_assigned_to(example_wallets_owner)

    # then
    assert len(result) == 3
