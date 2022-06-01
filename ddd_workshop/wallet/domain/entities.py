from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from bson.objectid import ObjectId

from ddd_workshop.building_blocks.custom_types import MongoDocument
from ddd_workshop.building_blocks.domain.entity import Entity
from ddd_workshop.wallet.domain.errors import InsufficientBalance, MaximumAmountExceeded, WrongCurrency
from ddd_workshop.wallet.domain.events import WalletBalanceDecreased, WalletBalanceIncreased, WalletCreated
from ddd_workshop.wallet.domain.value_objects import Currency, Money


@dataclass
class Wallet(Entity):
    _id: ObjectId
    _name: str
    _owner: ObjectId
    _balance: Money
    _created_at: datetime

    @classmethod
    def create(cls, name: str, owner: ObjectId, currency: Currency) -> "Wallet":
        wallet = cls(
            _domain_events=[],
            _id=ObjectId(),
            _name=name,
            _owner=owner,
            _balance=Money.zero(currency),
            _created_at=datetime.utcnow(),
        )
        wallet._add_domain_event(
            WalletCreated(
                id=ObjectId(),
                name="wallet.created",
                occurred_on=datetime.utcnow(),
                wallet_id=wallet._id,
                wallet_name=wallet._name,
            )
        )
        print(wallet)
        return wallet

    def increase_balance(self, amount: Money) -> None:
        if amount > Money.of(10000, amount.currency.value):
            raise MaximumAmountExceeded("Maximum amount is 1000")

        if amount.currency != self._balance.currency:
            raise WrongCurrency("Amount currency is different than wallet currency")

        self._balance = amount
        self._add_domain_event(
            WalletBalanceIncreased(
                id=ObjectId(),
                name="wallet.balance.increased",
                occurred_on=datetime.utcnow(),
                wallet_id=self._id,
                how_much=self._balance.amount,
                currency=self._balance.currency.value,
            )
        )

    def decrease_balance(self, amount: Money) -> None:
        if amount.currency != self._balance.currency:
            raise WrongCurrency("Amount currency is different than wallet currency")

        balance = self._balance - amount

        if balance < Money.zero(balance.currency):
            raise InsufficientBalance(
                f"Can not decrease balance by `{amount}` because the current balance is `{self._balance}`. Balance is not sufficient"
            )

        self._balance = balance

        self._add_domain_event(
            WalletBalanceDecreased(
                id=ObjectId(),
                name="wallet.balance.decreased",
                occurred_on=datetime.utcnow(),
                wallet_id=self._id,
                how_much=self._balance.amount,
                currency=self._balance.currency.value,
            )
        )

    def to_snapshot(self) -> Dict[str, Any]:
        return {
            "_id": self._id,
            "name": self._name,
            "owner": self._owner,
            "balance": {
                "amount": self._balance.amount,
                "currency": self._balance.currency.value,
            },
            "created_at": self._created_at,
        }

    @classmethod
    def from_snapshot(cls, document: MongoDocument) -> "Wallet":
        return cls(
            _domain_events=[],
            _id=document["_id"],
            _name=document["name"],
            _owner=document["owner"],
            _balance=Money.of(document["balance"]["amount"], document["balance"]["currency"]),
            _created_at=document["created_at"],
        )

    @property
    def id(self) -> ObjectId:
        return self._id

    @property
    def balance(self) -> Money:
        return self._balance
