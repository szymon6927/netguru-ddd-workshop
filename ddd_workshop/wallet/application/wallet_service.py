from kink import inject

from ddd_workshop.building_blocks.infrastructure.domain_event_publisher import IDomainEventPublisher
from ddd_workshop.wallet.domain.repository import IWalletRepository


@inject
class WalletService:
    def __init__(
        self,
        repository: IWalletRepository,
        domain_event_publisher: IDomainEventPublisher,
    ) -> None:
        self._repository = repository
        self._domain_event_publisher = domain_event_publisher
