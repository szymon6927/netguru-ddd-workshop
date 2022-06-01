from dataclasses import dataclass

from bson.objectid import ObjectId


@dataclass
class TransactionsHistory:
    wallet_id: ObjectId
