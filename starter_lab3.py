"""
starter_lab3.py — STARTER VERSION (Student Starter Code)

Module 3 Lab: Object-Oriented Python in Depth
"""

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
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    def __add__(self, other: "Money") -> "Money":
        raise NotImplementedError

    def __mul__(self, multiplier: int | Decimal) -> "Money":
        raise NotImplementedError

    __rmul__ = __mul__


class PositiveNumber:
    """Descriptor that validates assigned values are greater than zero."""

    def __set_name__(self, owner, name):
        raise NotImplementedError

    def __get__(self, instance, owner):
        raise NotImplementedError

    def __set__(self, instance, value):
        raise NotImplementedError


class Product:
    """Product with validated positive price and weight."""

    price = PositiveNumber()
    weight = PositiveNumber()

    def __init__(self, sku: str, name: str, price: Decimal, weight: float):
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError


@dataclass
class Customer:
    """Customer data model."""
    customer_id: str
    name: str
    email: str

    def __post_init__(self) -> None:
        raise NotImplementedError

    @property
    def domain(self) -> str:
        raise NotImplementedError


@dataclass
class OrderItem:
    """One product and quantity in an order."""
    product: Product
    quantity: int

    def __post_init__(self) -> None:
        raise NotImplementedError

    @property
    def subtotal(self) -> Money:
        raise NotImplementedError


class DiscountStrategy(ABC):
    """Abstract base class for discount behavior."""

    @abstractmethod
    def apply(self, subtotal: Money) -> Money:
        raise NotImplementedError


class NoDiscount(DiscountStrategy):
    """Discount strategy that returns subtotal unchanged."""

    def apply(self, subtotal: Money) -> Money:
        raise NotImplementedError


class PercentageDiscount(DiscountStrategy):
    """Percentage discount strategy."""

    def __init__(self, percent: Decimal):
        raise NotImplementedError

    def apply(self, subtotal: Money) -> Money:
        raise NotImplementedError


class Order:
    """Order composed of customer, line items, and discount strategy."""

    created_count = 0

    def __init__(
        self,
        order_id: str,
        customer: Customer,
        discount_strategy: Optional[DiscountStrategy] = None,
    ):
        raise NotImplementedError

    def add_item(self, product: Product, quantity: int) -> None:
        raise NotImplementedError

    @property
    def subtotal(self) -> Money:
        raise NotImplementedError

    @property
    def total(self) -> Money:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
