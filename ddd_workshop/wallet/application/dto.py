from dataclasses import dataclass

from bson.objectid import ObjectId


@dataclass
class CreateWalletDTO:
    name: str
    owner: ObjectId
    currency: str


@dataclass
class IncreaseBalanceDTO:
    wallet_id: ObjectId
    how_much: int
    currency: str


@dataclass
class DecreaseBalanceDTO:
    wallet_id: ObjectId
    how_much: int
    currency: str


@dataclass
class Transaction:
    wallet_id: ObjectId
    amount: int
    currency: str
    type: str
