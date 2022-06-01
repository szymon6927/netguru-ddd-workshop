from bson.objectid import ObjectId
from kink import inject

from ddd_workshop.building_blocks.infrastructure.domain_event_publisher import IDomainEventPublisher
from ddd_workshop.wallet.application.dto import CreateWalletDTO, DecreaseBalanceDTO, IncreaseBalanceDTO
from ddd_workshop.wallet.domain.entities import Currency, Wallet
from ddd_workshop.wallet.domain.repository import IWalletRepository
from ddd_workshop.wallet.domain.value_objects import Money


@inject
class WalletService:
    def __init__(
        self,
        repository: IWalletRepository,
        domain_event_publisher: IDomainEventPublisher,
    ) -> None:
        self._repository = repository
        self._domain_event_publisher = domain_event_publisher

    def get_wallet(self, wallet_id: ObjectId) -> Wallet:
        wallet = self._repository.get(wallet_id)
        return wallet

    def create_wallet(self, command: CreateWalletDTO) -> Wallet:
        wallet = Wallet.create(name=command.name, owner=command.owner, currency=Currency(command.currency))

        for event in wallet.events:
            print("event: ", event)
            self._domain_event_publisher.publish(event)

        self._repository.save(wallet)

        print(wallet.events)

        return wallet

    def increase_balance(self, request: IncreaseBalanceDTO) -> Wallet:
        wallet = self._repository.get(request.wallet_id)

        wallet.increase_balance(Money.of(request.how_much, request.currency))

        for event in wallet.events:
            self._domain_event_publisher.publish(event)

        self._repository.save(wallet)

        return wallet

    def decrease_balance(self, request: DecreaseBalanceDTO) -> Wallet:
        wallet = self._repository.get(request.wallet_id)

        wallet.decrease_balance(Money.of(request.how_much, request.currency))

        for event in wallet.events:
            self._domain_event_publisher.publish(event)

        self._repository.save(wallet)

        return wallet
