from bson.objectid import ObjectId
from pymongo.database import Database

from ddd_workshop.building_blocks.infrastructure.event_store import MongoEventStore
from ddd_workshop.wallet.application.query import TransactionsHistory
from ddd_workshop.wallet.application.query_handler import QueryHandler
from ddd_workshop.wallet.domain.entities import Wallet
from ddd_workshop.wallet.domain.value_objects import Currency, Money
from ddd_workshop.wallet.infrastructure.repository import MongoWalletRepository


def test_can_get_transactions_history(new_mongodb: Database) -> None:
    # given
    wallet = Wallet.create("test wallet", ObjectId(), currency=Currency.USD)
    event_store = MongoEventStore(new_mongodb)
    repo = MongoWalletRepository(new_mongodb)
    query_handler = QueryHandler(new_mongodb)

    # when
    wallet.increase_balance(Money.of(100, "USD"))
    wallet.increase_balance(Money.of(50, "USD"))
    wallet.decrease_balance(Money.of(50, "USD"))

    # and
    for event in wallet.events:
        event_store.save(event)
    repo.save(wallet)

    # when
    result = query_handler.get_transactions_history(TransactionsHistory(wallet_id=wallet.id))

    # then
    assert len(result) == 3
