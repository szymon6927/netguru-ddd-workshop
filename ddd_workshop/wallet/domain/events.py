from dataclasses import dataclass

from bson.objectid import ObjectId

from ddd_workshop.building_blocks.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class WalletCreated(DomainEvent):
    wallet_id: ObjectId
    wallet_name: str


@dataclass(frozen=True)
class WalletBalanceIncreased(DomainEvent):
    wallet_id: ObjectId
    how_much: int
    currency: str


@dataclass(frozen=True)
class WalletBalanceDecreased(DomainEvent):
    wallet_id: ObjectId
    how_much: int
    currency: str
