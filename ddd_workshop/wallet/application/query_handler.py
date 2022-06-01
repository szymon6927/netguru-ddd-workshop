from typing import List

import pymongo
from bson.objectid import ObjectId
from pymongo.database import Database

from ddd_workshop.wallet.application.dto import Transaction, Wallet
from ddd_workshop.wallet.application.query import TransactionsHistory


class QueryHandler:
    def __init__(self, database: Database):
        self._database = database

    def get_transactions_history(self, query: TransactionsHistory) -> List[Transaction]:
        result = []
        collection = self._database["events"]

        documents = collection.find(
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
        ).sort([("occurred_on", pymongo.ASCENDING)])

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

    def get_all_wallets_assigned_to(self, owner: ObjectId) -> List[Wallet]:
        result = []
        collection = self._database["wallets"]

        documents = collection.find({"owner": owner}).sort([("created_at", pymongo.ASCENDING)])

        for document in documents:
            result.append(
                Wallet(
                    id=document["_id"],
                    name=document["name"],
                    owner=document["owner"],
                    amount=document["balance"]["amount"],
                    currency=document["balance"]["currency"],
                )
            )

        return result
