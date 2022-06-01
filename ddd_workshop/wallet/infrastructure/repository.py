from bson.objectid import ObjectId
from kink import inject
from pymongo.database import Database

from ddd_workshop.wallet.domain.entities import Wallet
from ddd_workshop.wallet.domain.errors import WalletNotFound
from ddd_workshop.wallet.domain.repository import IWalletRepository


@inject(alias=IWalletRepository)
class MongoWalletRepository(IWalletRepository):
    def __init__(self, database: Database):
        self._collection = database["wallet"]

    def get(self, wallet_id: ObjectId) -> Wallet:
        document = self._collection.find_one({"_id": wallet_id})

        if not document:
            raise WalletNotFound(f"Wallet with id {wallet_id} does not exists!")

        return Wallet.from_snapshot(document)

    def save(self, wallet: Wallet) -> None:
        self._collection.update_one({"_id": wallet.id}, {"$set": wallet.to_snapshot()}, upsert=True)

        wallet.clear_domain_events()
