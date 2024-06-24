"""
All handy enums and module functions that can be used throughout the package.
"""

from __future__ import annotations

import enum
import functools
from collections.abc import Callable
from decimal import Decimal
from typing import Any


class RepaymentInterval(enum.Enum):
    """The interval over which the repayments are made."""

    YEARLY = enum.auto()
    MONTHLY = enum.auto()
    WEEKLY = enum.auto()
    DAILY = enum.auto()


class RepaymentFrequency(enum.Enum):
    """The frequency with which the repayments are made."""

    def __init__(
        self,
        repayment_unit: RepaymentInterval,
        repayment_frequency: int,
        total_repayments: int,
    ):
        """
        Defines a repayment schedule.

        :param repayment_unit: The calendar interval over which repayments are made.
        :param repayment_frequency: The number of calendar intervals between repayments.
        :param total_repayments: The total number of repayments.
        """
        self.repayment_unit = repayment_unit
        self.repayment_frequency = repayment_frequency
        self.total_repayments = total_repayments


class RepaymentType(enum.Enum):
    """
    Loan repayment types which determines the values of each repayment.

    Check the documentation of the corresponding loan objects for explanations
    of their differences.
    """

    FIXED_REPAYMENT = enum.auto()
    FIXED_PRINCIPAL = enum.auto()
    INTEREST_ONLY = enum.auto()


class InterestRateType(enum.Enum):
    """
    Loan interest rate types.

    - VARIABLE: A variable rate can change over the lifetime of the loan. This
      is usually when the interest rate is tied to a benchmark rate that also
      changes over time, such as the Bank of England rate.

    - FIXED: A fixed rate does not change over the lifetime of the loan.
    """

    VARIABLE = enum.auto()
    FIXED = enum.auto()


class InterestApplyMethod(enum.Enum):
    """
    Whether the interest is applied before or after the repayment.
    """

    BEFORE = 0
    AFTER = 1


def _to_decimal(value: Any) -> Decimal:
    """
    Casting a float directly to a decimal messes with the precision so casting
    to a string first is preferable.
    """
    # Purposely pass None into Decimal to generate the correct error
    return Decimal(None) if value is None else Decimal(str(value))  # noqa


def _decimal(round_to: int | None = None) -> Callable:
    """
    Decorator for the `_to_decimal` function with an optional precision to round
    to.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if round_to is None:
                return _to_decimal(func(*args, **kwargs))
            return _to_decimal(round(func(*args, **kwargs), round_to))

        return wrapper

    return decorator


def _calculate_amortised_rate(interest_rate: Decimal, n: Decimal) -> Decimal:
    """
    Calculate the amortised rate at `n`.

    Let :math:`R` be the interest rate on a loan. Then the amortised rate is
    given by :math:`(1 + R)^{n}`.
    """
    if n is None:
        return Decimal(1)
    if n < 0:
        raise AssertionError("The amortise rate period has to be positive.")
    return _to_decimal((Decimal(1) + interest_rate) ** n)
