from abc import ABC, abstractmethod

from kink import inject

from ddd_workshop.building_blocks.domain.domain_event import DomainEvent
from ddd_workshop.building_blocks.infrastructure.event_store import IEventStore


class IDomainEventPublisher(ABC):
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        pass


@inject
class StoreAndForwardDomainEventPublisher(IDomainEventPublisher):
    def __init__(self, event_store: IEventStore) -> None:
        self._event_store = event_store

    def publish(self, event: DomainEvent) -> None:
        self._event_store.save(event)

    def publish_all_periodically(self) -> None:
        pass
