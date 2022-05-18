from bson.objectid import ObjectId
from kink import inject
from pymongo.database import Database

from ddd_workshop.wallet.domain.entities import Wallet
from ddd_workshop.wallet.domain.repository import IWalletRepository


@inject(alias=IWalletRepository)
class MongoWalletRepository(IWalletRepository):
    def __init__(self, database: Database):
        self._collection = database["wallet"]

    def get(self, wallet_id: ObjectId) -> Wallet:
        pass

    def save(self, wallet: Wallet) -> None:
        pass
