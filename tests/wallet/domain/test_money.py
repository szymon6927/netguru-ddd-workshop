import pytest

from ddd_workshop.wallet.domain.errors import WrongCurrency
from ddd_workshop.wallet.domain.value_objects import Currency, Money


def test_can_compare_money() -> None:
    # expect
    assert Money.of(100, Currency.EUR.value) == Money.of(100, Currency.EUR.value)
    assert Money.of(150, Currency.USD.value) > Money.of(100, Currency.USD.value)
    assert Money.of(50, Currency.GBP.value) < Money.of(100, Currency.GBP.value)


def test_can_add() -> None:
    # expect
    assert Money.of(100, Currency.GBP.value) + Money.of(50, Currency.GBP.value) == Money.of(150, Currency.GBP.value)
    with pytest.raises(WrongCurrency):
        Money.of(100, Currency.GBP.value) + Money.of(100, Currency.USD.value)


def test_can_sub() -> None:
    # expect
    assert Money.of(100, Currency.GBP.value) - Money.of(50, Currency.GBP.value) == Money.of(50, Currency.GBP.value)
    with pytest.raises(WrongCurrency):
        Money.of(100, Currency.GBP.value) - Money.of(100, Currency.USD.value)


def test_can_multiply() -> None:
    assert Money.of(50, Currency.GBP.value) * Money.of(50, Currency.GBP.value) == Money.of(2500, Currency.GBP.value)
    with pytest.raises(WrongCurrency):
        Money.of(10, Currency.USD.value) * Money.of(10, Currency.GBP.value)
