import pytest
from bson.objectid import ObjectId

from ddd_workshop.wallet.domain.entities import Wallet
from ddd_workshop.wallet.domain.errors import InsufficientBalance, MaximumAmountExceeded, WrongCurrency
from ddd_workshop.wallet.domain.value_objects import Currency, Money


def test_can_increase_balance() -> None:
    # given
    wallet = Wallet.create(name="test", owner=ObjectId(), currency=Currency.USD)

    # when
    wallet.increase_balance(Money.of(100, Currency.USD.value))

    # then
    assert wallet.balance == Money.of(100, Currency.USD.value)
    assert len(wallet.events) == 2


def test_increasing_balance_works_only_with_single_currency() -> None:
    # given
    wallet = Wallet.create(name="test", owner=ObjectId(), currency=Currency.USD)

    # expect
    with pytest.raises(WrongCurrency):
        wallet.increase_balance(Money.of(1000, Currency.EUR.value))


def test_can_check_maximum_amount() -> None:
    # given
    wallet = Wallet.create(name="test", owner=ObjectId(), currency=Currency.USD)

    # expect
    with pytest.raises(MaximumAmountExceeded):
        wallet.increase_balance(Money.of(10001, Currency.USD.value))


def test_can_decrease_balance() -> None:
    # given
    wallet = Wallet.create(name="test", owner=ObjectId(), currency=Currency.USD)

    # when
    wallet.increase_balance(Money.of(100, Currency.USD.value))

    # and
    wallet.decrease_balance(Money.of(50, Currency.USD.value))

    # then
    assert wallet.balance == Money.of(50, Currency.USD.value)


def test_can_not_decrease_balance_to_negative_value() -> None:
    # given
    wallet = Wallet.create(name="test", owner=ObjectId(), currency=Currency.USD)

    # when
    wallet.increase_balance(Money.of(100, Currency.USD.value))

    # then
    with pytest.raises(InsufficientBalance):
        wallet.decrease_balance(Money.of(150, Currency.USD.value))
