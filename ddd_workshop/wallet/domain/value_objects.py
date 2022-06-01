from dataclasses import dataclass
from enum import Enum, unique

from ddd_workshop.wallet.domain.errors import WrongCurrency


@unique
class Currency(Enum):
    GBP = "GBP"
    USD = "USD"
    EUR = "EUR"


@dataclass(frozen=True)
class Money:
    amount: int
    currency: Currency

    def __add__(self, other: "Money") -> "Money":
        if other.currency != self.currency:
            raise WrongCurrency("Can not add money with different currency!")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if other.currency != self.currency:
            raise WrongCurrency("Can not subtract money with different currency!")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, other: "Money") -> "Money":
        if other.currency != self.currency:
            raise WrongCurrency("Can not multiply money with different currency!")

        return Money(self.amount * other.amount, self.currency)

    def __lt__(self, other: "Money") -> bool:
        return self.amount < other.amount and self.currency == other.currency

    def __le__(self, other: "Money") -> bool:
        return self.amount <= other.amount and self.currency == other.currency

    def __ge__(self, other: "Money") -> bool:
        return self.amount >= other.amount and self.currency == other.currency

    def __gt__(self, other: "Money") -> bool:
        return self.amount > other.amount and self.currency == other.currency

    def __str__(self) -> str:
        return f"{self.amount} ({self.currency.value})"

    @classmethod
    def zero(cls, currency: Currency) -> "Money":
        return cls(0, currency)

    @classmethod
    def of(cls, value: int, currency: str) -> "Money":
        return cls(value, Currency(currency))
