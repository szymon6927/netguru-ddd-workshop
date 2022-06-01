from ddd_workshop.building_blocks.domain.errors import DomainError


class WrongCurrency(DomainError):
    pass


class MaximumAmountExceeded(DomainError):
    pass


class InsufficientBalance(DomainError):
    pass


class WalletNotFound(DomainError):
    pass
