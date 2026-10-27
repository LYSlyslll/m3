"""Module 3 Lab: Order Processing System."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class Money:
    """Immutable value object representing money."""

    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            raise TypeError("amount must be a Decimal")

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"

    def __add__(self, other: Money) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, multiplier: int | Decimal) -> Money:
        if not isinstance(multiplier, (int, Decimal)):
            return NotImplemented
        return Money(self.amount * multiplier, self.currency)

    __rmul__ = __mul__


class PositiveNumber:
    """Descriptor that validates assigned values are greater than zero."""

    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        if not value > 0:
            raise ValueError(f"{self.private_name[1:]} must be greater than zero")
        setattr(instance, self.private_name, value)


class Product:
    """Product with validated positive price and weight."""

    price = PositiveNumber()
    weight = PositiveNumber()

    def __init__(self, sku: str, name: str, price: Decimal, weight: float):
        self.sku = sku
        self.name = name
        self.price = price
        self.weight = weight

    def __repr__(self) -> str:
        return (
            f"Product(sku={self.sku!r}, name={self.name!r}, "
            f"price={self.price!r}, weight={self.weight!r})"
        )

    def __str__(self) -> str:
        return f"{self.name} ({self.sku}): {self.price:.2f}"


@dataclass
class Customer:
    """Customer data model."""

    customer_id: str
    name: str
    email: str

    def __post_init__(self) -> None:
        if "@" not in self.email:
            raise ValueError("email must contain '@'")

    @property
    def domain(self) -> str:
        return self.email.split("@", 1)[1]


@dataclass
class OrderItem:
    """One product and quantity in an order."""

    product: Product
    quantity: int

    def __post_init__(self) -> None:
        if not self.quantity > 0:
            raise ValueError("quantity must be greater than zero")

    @property
    def subtotal(self) -> Money:
        return Money(self.product.price * self.quantity)


class DiscountStrategy(ABC):
    """Abstract base class for discount behavior."""

    @abstractmethod
    def apply(self, subtotal: Money) -> Money:
        ...


class NoDiscount(DiscountStrategy):
    """Discount strategy that returns subtotal unchanged."""

    def apply(self, subtotal: Money) -> Money:
        return subtotal


class PercentageDiscount(DiscountStrategy):
    """Percentage discount strategy."""

    def __init__(self, percent: Decimal):
        if not 0 <= percent <= 100:
            raise ValueError("percent must be between 0 and 100 inclusive")
        self.percent = percent

    def apply(self, subtotal: Money) -> Money:
        return subtotal * (Decimal("1") - self.percent / Decimal("100"))


class Order:
    """Order composed of customer, line items, and discount strategy."""

    created_count = 0

    def __init__(
        self,
        order_id: str,
        customer: Customer,
        discount_strategy: Optional[DiscountStrategy] = None,
    ):
        self.order_id = order_id
        self.customer = customer
        self.discount_strategy = (
            NoDiscount() if discount_strategy is None else discount_strategy
        )
        self.items: list[OrderItem] = []
        Order.created_count += 1

    def add_item(self, product: Product, quantity: int) -> None:
        self.items.append(OrderItem(product, quantity))

    @property
    def subtotal(self) -> Money:
        return sum((item.subtotal for item in self.items), Money(Decimal("0")))

    @property
    def total(self) -> Money:
        return self.discount_strategy.apply(self.subtotal)

    def __repr__(self) -> str:
        return (
            f"Order(order_id={self.order_id!r}, customer={self.customer!r}, "
            f"items={self.items!r}, discount_strategy={self.discount_strategy!r})"
        )

    def __str__(self) -> str:
        return (
            f"Order {self.order_id} for {self.customer.name}: "
            f"{len(self.items)} item(s), total {self.total}"
        )
