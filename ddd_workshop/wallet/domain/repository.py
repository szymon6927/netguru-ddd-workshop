from abc import ABC, abstractmethod

from bson.objectid import ObjectId

from ddd_workshop.wallet.domain.entities import Wallet


class IWalletRepository(ABC):
    @abstractmethod
    def get(self, wallet_id: ObjectId) -> Wallet:
        pass

    @abstractmethod
    def save(self, wallet: Wallet) -> None:
        pass
