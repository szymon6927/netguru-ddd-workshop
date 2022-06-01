from typing import List

from pymongo.database import Database

from ddd_workshop.wallet.application.dto import Transaction
from ddd_workshop.wallet.application.query import TransactionsHistory


class QueryHandler:
    def __init__(self, database: Database):
        self._collection = database["events"]

    def get_transactions_history(self, query: TransactionsHistory) -> List[Transaction]:
        result = []

        documents = self._collection.find(
            {
                "$and": [
                    {"data.wallet_id": query.wallet_id},
                    {
                        "$or": [
                            {"name": "wallet.balance.increased"},
                            {"name": "wallet.balance.decreased"},
                        ]
                    },
                ]
            }
        )

        # print(list(documents))

        for document in documents:
            transaction_type = "+" if document["name"] == "wallet.balance.increased" else "-"
            result.append(
                Transaction(
                    wallet_id=document["data"]["wallet_id"],
                    amount=document["data"]["how_much"],
                    currency=document["data"]["currency"],
                    type=transaction_type,
                )
            )

        return result
