from dataclasses import dataclass
from typing import List

from ddd_workshop.building_blocks.domain.domain_event import DomainEvent


@dataclass
class Entity:
    _domain_events: List[DomainEvent]

    def clear_domain_events(self) -> None:
        self._domain_events.clear()

    def _add_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    @property
    def events(self) -> List[DomainEvent]:
        return self._domain_events[:]
