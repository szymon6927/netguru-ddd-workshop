from unittest.mock import Mock

from ddd_workshop.building_blocks.domain.domain_event import DomainEvent
from ddd_workshop.building_blocks.infrastructure.domain_event_publisher import StoreAndForwardDomainEventPublisher
from ddd_workshop.building_blocks.infrastructure.event_store import IEventStore


def test_can_publish_event(workshop_started_test_event: DomainEvent) -> None:
    # given
    event_store = Mock(spec_set=IEventStore)
    event_publisher = StoreAndForwardDomainEventPublisher(event_store)

    # when
    event_publisher.publish(workshop_started_test_event)

    # then
    event_store.save.assert_called_once_with(workshop_started_test_event)
