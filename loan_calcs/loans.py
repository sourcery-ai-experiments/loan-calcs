"""
Different types of loans and ways to set them up.
"""

from __future__ import annotations

import abc
import math
from decimal import Decimal
from typing import Self

from loan_calcs.data import (
    InterestApplyMethod,
    InterestRateType,
    RepaymentType,
    _calculate_amortised_rate,
    _to_decimal,
)


# sourcery skip: snake-case-functions
class Loan(abc.ABC):
    """
    A loan, which is a fixed value of money borrowed by an entity and
    usually repaid over a series of instalments.

    The following notation is used throughout the Loan classes:
        * :math:`L`: Loan amount.
        * :math:`R`: Periodic interest rate.
        * :math:`N`: Total number of repayments.
        * :math:`P`: Total periodic repayment value (the principal part has
                     a subscript :math:`p`, :math:`P_{p}`).
        * :math:`b`: Whether the interest is applied before or after the
                     repayment.
        * :math:`B_n`: The balance on the loan at period :math:`n`.

    The repayment for a loan typically has (at least) 2 components:
        * The *principal* part, which is paying off the original money that
          was borrowed.
        * The *interest* part, which is paying off the interest applied on
          the loan.

    In 'real life', a loan can have other components such as fees. These are
    outside the scope of these objects.
    """

    type: RepaymentType = NotImplemented

    def __init__(
        self,
        *,
        loan_amount: Decimal,
        interest_rate: Decimal,
        total_repayments: Decimal,
        fixed_periodic_repayment: Decimal,
        before_or_after: InterestApplyMethod = InterestApplyMethod.BEFORE,
        interest_rate_type: InterestRateType = InterestRateType.VARIABLE,
    ) -> None:
        """
        Create a loan.

        The `fixed_periodic_repayment` argument depends on the loan type:
            * For a fixed repayment loan, this corresponds to the total
              repayment value.
            * For a fixed principal loan, this corresponds to the principal part
              of the repayment value.
        """
        self.interest_rate_type = interest_rate_type
        self.before_or_after = before_or_after
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.total_repayments = total_repayments
        self.periodic_repayment = fixed_periodic_repayment

    @classmethod
    def build__all(
        cls,
        *,
        loan_amount: Decimal | float,
        interest_rate: Decimal | float,
        total_repayments: Decimal | int,
        fixed_periodic_repayment: Decimal | float,
        before_or_after: InterestApplyMethod = InterestApplyMethod.BEFORE,
        interest_rate_type: InterestRateType = InterestRateType.VARIABLE,
    ) -> Self:
        """
        Build the loan using all 4 of the key components.
        """
        return cls(
            loan_amount=_to_decimal(loan_amount),
            interest_rate=_to_decimal(interest_rate),
            total_repayments=_to_decimal(total_repayments),
            fixed_periodic_repayment=_to_decimal(fixed_periodic_repayment),
            before_or_after=before_or_after,
            interest_rate_type=interest_rate_type,
        )

    @classmethod
    def build(
        cls,
        *,
        loan_amount: Decimal | float | None = None,
        interest_rate: Decimal | float | None = None,
        total_repayments: Decimal | int | None = None,
        fixed_periodic_repayment: Decimal | float | None = None,
        before_or_after: InterestApplyMethod = InterestApplyMethod.BEFORE,
        interest_rate_type: InterestRateType = InterestRateType.VARIABLE,
    ) -> Self:
        """
        Create a loan.

        The `fixed_periodic_repayment` argument depends on the loan type:
            * For a fixed repayment loan, this corresponds to the total
              repayment value.
            * For a fixed principal loan, this corresponds to the principal part
              of the repayment value.
        """
        kwargs = {
            "loan_amount": _to_decimal(loan_amount) if loan_amount else None,
            "interest_rate": _to_decimal(interest_rate) if interest_rate else None,
            "total_repayments": int(total_repayments) if total_repayments else None,
            "fixed_periodic_repayment": (
                _to_decimal(fixed_periodic_repayment)
                if fixed_periodic_repayment
                else None
            ),
            "before_or_after": before_or_after,
            "interest_rate_type": interest_rate_type,
            "total_amortised_rate": _calculate_amortised_rate(
                interest_rate=_to_decimal(interest_rate) if interest_rate else None,
                n=total_repayments,
            ),
        }

        if None not in (
            loan_amount,
            interest_rate,
            total_repayments,
            fixed_periodic_repayment,
        ):
            raise ValueError("No validation for all not None arguments yet.")

        if loan_amount is None:
            assert None not in (
                interest_rate,
                total_repayments,
                fixed_periodic_repayment,
            )
            loan_amount = cls._build__calculate_loan_amount(**kwargs)
        elif interest_rate is None:
            assert None not in (loan_amount, total_repayments, fixed_periodic_repayment)
            interest_rate = cls._build__calculate_interest_rate(**kwargs)
        elif total_repayments is None:
            assert None not in (loan_amount, interest_rate, fixed_periodic_repayment)
            total_repayments = cls._build__calculate_total_repayments(**kwargs)
        elif fixed_periodic_repayment is None:
            assert None not in (loan_amount, interest_rate, total_repayments)
            fixed_periodic_repayment = cls._build__calculate_fixed_periodic_repayment(
                **kwargs
            )
        else:
            raise ValueError("Something has gone really wrong.")

        return cls.build__all(
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            total_repayments=total_repayments,
            fixed_periodic_repayment=fixed_periodic_repayment,
            before_or_after=before_or_after,
            interest_rate_type=interest_rate_type,
        )

    @property
    def total_amortised_rate(self) -> Decimal:
        """
        Calculate the amortised rate at the complete term.
        """
        return _calculate_amortised_rate(self.interest_rate, self.total_repayments)

    @classmethod
    def _build__calculate_loan_amount(cls, **kwargs) -> Decimal:
        """
        Calculate the loan amount, :math:`L`.
        """
        raise NotImplementedError(
            f"{cls}._build__calculate_loan_amount has not been defined"
        )

    @classmethod
    def _build__calculate_interest_rate(cls, **kwargs) -> Decimal:
        """
        Calculate the loan interest rate, :math:`R`.
        """
        raise NotImplementedError(
            f"{cls}._build__calculate_interest_rate has not been defined"
        )

    @classmethod
    def _build__calculate_fixed_periodic_repayment(cls, **kwargs) -> Decimal:
        """
        Calculate the periodic repayment value, :math:`P`.
        """
        raise NotImplementedError(
            f"{cls}._build__calculate_fixed_periodic_repayment has not been defined"
        )

    @classmethod
    def _build__calculate_total_repayments(cls, **kwargs) -> Decimal:
        """
        Calculate the total number of repayments, :math:`N`.
        """
        raise NotImplementedError(
            f"{cls}._build__calculate_total_repayments has not been defined"
        )

    @abc.abstractmethod
    def calculate_balance_at_period(self, period: int) -> Decimal:
        """
        Calculate the loan balance, :math:`B_{n}`, at the end of period
        :math:`n`.
        """

    @abc.abstractmethod
    def calculate_repayment_principal_at_period(self, period: int) -> Decimal:
        """
        Calculate the principal part of the repayment due on period :math:`n`.
        """

    @abc.abstractmethod
    def calculate_repayment_interest_at_period(self, period: int) -> Decimal:
        """
        Calculate the interest part of the repayment due on period :math:`n`.
        """

    @abc.abstractmethod
    def calculate_cumulative_interest(self, period: int) -> Decimal:
        """
        Calculate the total of the interest that has been accrued (including the
        interest that has been paid off) at the end of period :math:`n`.

        In Financial terms, this is called the "interest income" (for the
        bank/entity that issued the loan).
        """


class FixedRepaymentLoan(Loan):
    """
    A fixed repayment loan.

    A fixed repayment loan is the 'normal' type of loan: each repayment pays
    off some original loan amount but also some interest. Each repayment has
    the same value.
    """

    type = RepaymentType.FIXED_REPAYMENT

    @staticmethod
    # @_decimal(round_to=2)
    def _build__calculate_loan_amount(
        interest_rate: Decimal,
        fixed_periodic_repayment: Decimal,
        total_amortised_rate: Decimal,
        before_or_after: InterestApplyMethod = InterestApplyMethod.BEFORE,
        **kwargs,  # To allow other arguments to be passed in without breaking the interface
    ) -> Decimal:
        """
        Calculate the loan amount, :math:`L`.

        This uses the interest rate (:math:`R`), total repayments (:math:`N`),
        the period repayment (:math:`P`), and whether the interest is applied
        before or after the repayment (:math:`b`).

        The loan value, :math:`L`, for a fixed repayment loan is:

        ..  math::

            L = \\frac{ PR^{b - 1}((1 + R)^{N} - 1) }{ (1 + R)^{N} }
        """
        return (
            fixed_periodic_repayment
            * (interest_rate ** (before_or_after.value - Decimal(1)))
            * (total_amortised_rate - Decimal(1))
            / total_amortised_rate
        )

    # @staticmethod
    # @_decimal(round_to=2)
    def _build__calculate_interest_rate(self) -> Decimal:
        """
        Calculate the loan interest rate, :math:`R`.
        """
        raise NotImplementedError(
            f"{type(self).__name__}._build__calculate_interest_rate has not been defined"
        )

    @staticmethod
    # @_decimal(round_to=2)
    def _build__calculate_fixed_periodic_repayment(
        loan_amount: Decimal,
        interest_rate: Decimal,
        total_amortised_rate: Decimal,
        before_or_after: InterestApplyMethod = InterestApplyMethod.BEFORE,
        **kwargs,  # To allow other arguments to be passed in without breaking the interface
    ) -> Decimal:
        """
        Calculate the period repayment (:math:`P`).

        This uses the interest rate (:math:`R`), total repayments (:math:`N`),
        loan amount (:math:`L`), and whether the interest is applied before or
        after the repayment (:math:`b`).

        The period repayment value, :math:`P`, for a fixed total repayment value
        is:

        ..  math::

            P = \\frac{ LR^{1 - b}(1 + R)^{N} }{ (1 + R)^{N} - 1 }
        """
        return (
            (interest_rate ** (Decimal(1) - before_or_after.value))
            * loan_amount
            * total_amortised_rate
            / (total_amortised_rate - Decimal(1))
        )

    @staticmethod
    # @_decimal()
    def _build__calculate_total_repayments(
        loan_amount: Decimal,
        fixed_periodic_repayment: Decimal,
        interest_rate: Decimal,
        before_or_after: InterestApplyMethod = InterestApplyMethod.BEFORE,
        **kwargs,  # To allow other arguments to be passed in without breaking the interface
    ) -> int:
        """
        Calculate the total repayments, :math:`N`.

        This uses the interest rate (:math:`R`), period repayment (:math:`R`),
        loan amount (:math:`L`), and whether the interest is applied before or
        after the repayment (:math:`b`).

        The natural log form of the calculation for the total repayments,
        :math:`N`, of a fixed repayment loan is:

        ..  math::

            N = \\frac{ \\ln(P / (P - LR^{1 - b}) }{ \\ln(1 + R) }

        The expression :math:`P - LR^{1 - b}` has to be strictly positive,
        otherwise there would be an unbounded number of repayments.
        """
        denominator = Decimal(
            fixed_periodic_repayment
            - loan_amount * interest_rate ** (Decimal(1) - before_or_after.value)
        )

        if denominator <= 0:
            # return math.inf
            raise ValueError(
                "The values of the loan amount, interest rate, and periodic"
                " repayment lead to an unbounded number of repayments."
            )

        return math.ceil(
            math.log(fixed_periodic_repayment / denominator)
            / math.log(interest_rate + Decimal(1))
        )

    # @_decimal(round_to=2)
    def calculate_balance_at_period(self, period: int) -> Decimal:
        """
        Calculate the loan balance, :math:`B_{n}`, at the end of period
        :math:`n`.

        The balance at the end of period :math:`n`, :math:`b_{n}`, for a fixed
        repayment loan is:

        ..  math::

            B_{n} = L(1 + R)^{n} - PR^{b - 1}((1 + R)^{n} - 1)
        """
        amortised_rate = _calculate_amortised_rate(
            self.interest_rate, _to_decimal(period)
        )  # (1 + R)^{n}
        return self.loan_amount * amortised_rate - (
            self.periodic_repayment
            * (self.interest_rate ** (self.before_or_after.value - 1))
            * (amortised_rate - Decimal(1))
        )

    # @_decimal(round_to=2)
    def calculate_repayment_principal_at_period(self, period: int) -> Decimal:
        """
        Calculate the principal part of the repayment due on period :math:`n`.

        For a fixed repayment loan, the principal part of the repayment due on
        period :math:`n` is:

        ..  math::

            P_{P, n} = P - P_{I, n} = P - B_{n - 1}R

        This expands out to the following (although this isn't being used):

        ..  math::

            P_{P, n} = P + PR^{b}((1 + R)^{n - 1} - 1) - LR(1 + R)^{n - 1}
        """
        return self.periodic_repayment - self.calculate_repayment_interest_at_period(
            period=period
        )

    # @_decimal(round_to=2)
    def calculate_repayment_interest_at_period(self, period: int) -> Decimal:
        """
        Calculate the interest part of the repayment due on period :math:`n`.

        For a fixed repayment loan, the interest part of the repayment due on
        period :math:`n` is:

        ..  math::

            P_{I, n} = B_{n - 1}R

        This expands out to the following (although this isn't being used):

        ..  math::

            P_{I, n} = LR(1 + R)^{n - 1} - PR^{b}((1 + R)^{n - 1} - 1)
        """
        return self.calculate_balance_at_period(period=period - 1) * self.interest_rate

    # @_decimal(round_to=2)
    def calculate_cumulative_interest(self, period: int) -> Decimal:
        """
        Calculate the cumulative interest accrued at the end of period
        :math:`n`.

        The cumulative interest accrued at the end of period :math:`n` for a
        fixed repayment loan is:

        ..  math::

            I_{n} = TODO: formula here, also decide on notation for this (\\sum I_{k} or I_{n})
        """
        raise NotImplementedError(
            f"{type(self).__name__}.calculate_cumulative_interest has not been defined"
        )


class FixedPrincipalLoan(Loan):
    """
    A fixed principal loan.

    A fixed principal loan is similar to a fixed repayment loan where each
    repayment pays off some original loan amount and also some interest.
    However, only the principal part of each repayment has the same value.

    TODO: A fixed principal loan should only have `before_or_after = BEFORE`
          but can we account for the other case? The solution looks tricky
          to find analytically, so might need a numerical solution.
    """

    type = RepaymentType.FIXED_PRINCIPAL

    @property
    def principal_repayment(
        self,
        custom_periodic_repayment: Decimal | None = None,
    ) -> Decimal:
        """
        Calculate the principal component of the period repayment.

        Note that, for the fixed principal loan, we could have 2 scenarios:
            1. The periodic principal is the loan value divided by the number of
               repayments, :math:`L/N`
            2. The periodic principal is a fixed amount, with the difference
               added on the final repayment (the balloon)
        """
        calculated_principal_repayment = self.loan_amount / self.total_repayments
        if custom_periodic_repayment is None:
            return calculated_principal_repayment

        if custom_periodic_repayment > calculated_principal_repayment:
            raise ValueError(
                f"The custom periodic repayment amount, {custom_periodic_repayment:.4f}, exceeds the maximum value "
                f"allowed by the loan value and the number of repayments, {calculated_principal_repayment:.4f}"
            )

        return custom_periodic_repayment

    @staticmethod
    # @_decimal(round_to=2)
    def _build__calculate_loan_amount(
        total_repayments: int,
        fixed_periodic_repayment: Decimal,
        custom_loan_amount: Decimal = None,
        **kwargs,  # To allow other arguments to be passed in without breaking the interface
    ) -> Decimal:
        """
        Calculate the loan amount, :math:`L`.

        Similar to how the principal repayment isn't necessarily computed using
        the loan amount, the loan amount also isn't necessarily computed using
        the principal repayment. Again, there are 2 scenarios:
            1. The loan value is the periodic principal multiplied by the number
               of repayments, :math:`PN`.
            2. The loan value is a fixed amount, with lower value period
               repayments and a larger final repayment.
        """
        calculated_loan_amount = fixed_periodic_repayment * total_repayments
        if custom_loan_amount is None:
            return calculated_loan_amount

        if custom_loan_amount > calculated_loan_amount:
            raise ValueError(
                f"The custom loan amount, {custom_loan_amount:.4f}, exceeds the minimum value allowed by the principal "
                f"repayment amount and the number of repayments, {calculated_loan_amount:.4f}"
            )

        return custom_loan_amount

    # @staticmethod
    # @_decimal(round_to=2)
    def _build__calculate_interest_rate(self) -> Decimal:
        """
        Calculate the loan interest rate, :math:`R`.
        """
        raise NotImplementedError(
            f"{type(self).__name__}._build__calculate_interest_rate has not been defined"
        )

    @staticmethod
    # @_decimal(round_to=2)
    def _build__calculate_fixed_periodic_repayment(
        loan_amount: Decimal,
        total_repayments: int,
        custom_periodic_repayment: Decimal = None,
        **kwargs,  # To allow other arguments to be passed in without breaking the interface
    ) -> Decimal:
        """
        Calculate the period repayment, :math:`P`.

        The period repayment value, :math:`P`, for a fixed principal loan is:

        ..  math::

            P = L/N + interest amount

        TODO: Determine the interest amount -- or, adjust to be more like the
              init args. ie this calcs the corresponding fixed value, but also
              there is a method for repayment due at `n`.

        TODO: This should only be the fixed amount, not the fixed amount plus
              the interest amount.

        Note that, for the fixed principal loan, we could have 2 scenarios:
            1. The periodic principal is the loan value divided by the number of
               repayments (as above)
            2. The periodic principal is a fixed amount, with the difference
               added on the final repayment (the balloon)
        """
        calculated_periodic_repayment = loan_amount / total_repayments
        if custom_periodic_repayment is None:
            return calculated_periodic_repayment

        if custom_periodic_repayment > calculated_periodic_repayment:
            raise ValueError(
                f"The custom periodic repayment amount, {custom_periodic_repayment:.4f}, exceeds the maximum value "
                f"allowed by the loan value and the number of repayments, {calculated_periodic_repayment:.4f}"
            )

        return custom_periodic_repayment

    @staticmethod
    # @_decimal()
    def _build__calculate_total_repayments(
        loan_amount: Decimal,
        fixed_periodic_repayment: Decimal,  # This is actually the principal repayment
        custom_total_repayments: int = None,
        **kwargs,  # To allow other arguments to be passed in without breaking the interface
    ) -> int:
        """
        Calculate the total repayments, :math:`N`.

        Similar to how the loan amount isn't necessarily computed the principal
        repayment amount, the total repayments also isn't necessarily computed
        using the other components of the loan. Again, there are 2 scenarios:
            1.  The total repayments is the loan amount divided by the periodic
                principal, :math:`L/P`.
            2.  The total repayments is a fixed amount, with lower value period
                repayments and a larger final repayment.
        """
        calculated_total_repayments = math.ceil(loan_amount / fixed_periodic_repayment)
        if custom_total_repayments is None:
            return calculated_total_repayments

        if custom_total_repayments > calculated_total_repayments:
            raise ValueError(
                f"The custom number of repayments, {custom_total_repayments:.4f}, exceeds the maximum value "
                f"allowed by the loan value and the principal repayment value, {calculated_total_repayments:.4f}"
            )

        return custom_total_repayments

    # @_decimal(round_to=2)
    def calculate_balance_at_period(self, period: Decimal) -> Decimal:
        """
        Calculate the loan balance, :math:`B_{n}`, at the end of period
        :math:`n`.

        The balance at the end of period :math:`n`, :math:`B_{n}`, for a fixed
        principal loan is simple when the interest is added before the repayment
        is made. Each repayment is simply the fixed principal amount, plus the
        interest accrued in that period. Therefore, the balance is simply the
        starting balance (the loan amount, :math:`L`) subtract the product of
        the fixed principal amount (:math:`P_{p}`) and the number of periods
        (:math:`n`).

        ..  math::

            B_{n} = L - n * P_{p}
        """
        return self.loan_amount - (period * self.principal_repayment)

    # @_decimal(round_to=2)
    def calculate_repayment_principal_at_period(self, period: int) -> Decimal:
        """"""
        raise NotImplementedError(
            f"{type(self).__name__}.calculate_repayment_principal_at_period has not been defined"
        )

    # @_decimal(round_to=2)
    def calculate_repayment_interest_at_period(self, period: int) -> Decimal:
        """"""
        raise NotImplementedError(
            f"{type(self).__name__}.calculate_repayment_interest_at_period has not been defined"
        )

    # @_decimal(round_to=2)
    def calculate_cumulative_interest(self, period: int) -> Decimal:
        """
        Calculate the cumulative interest accrued at the end of period
        :math:`n`.

        The cumulative interest accrued at the end of period :math:`n` for a
        fixed principal loan is:

        ..  math::

            I_{n} = TODO: formula here, also decide on notation for this (\\sum I_{k} or I_{n})
        """


class InterestOnlyLoan(Loan):
    """
    An interest-only loan.

    An interest-only loan is where each periodic repayment only pays off the
    accrued interest on the loan. The principal value of the loan is paid
    off in the final repayment.

    TODO: An interest-only loan is just a special case of a fixed principal
          loan (fixed principal = 0).
    TODO: An interest-only loan can only have `before_or_after = BEFORE`.
    """

    type = RepaymentType.INTEREST_ONLY

    @staticmethod
    # @_decimal(round_to=2)
    def _build__calculate_loan_amount(
        fixed_periodic_repayment: Decimal,
        interest_rate: Decimal,
        **kwargs,  # To allow other arguments to be passed in without breaking the interface
    ) -> Decimal:
        """
        Calculate the loan amount, :math:`L`.

        This uses the interest rate (:math:`R`) and the period repayment
        (:math:`P`).

        The loan value, :math:`L`, for an interest-only loan is:

        ..  math::

            L = P/R
        """
        return fixed_periodic_repayment / interest_rate

    # @staticmethod
    # @_decimal(round_to=2)
    def _build__calculate_interest_rate(self) -> Decimal:
        """
        Calculate the loan interest rate, :math:`R`.
        """
        raise NotImplementedError(
            f"{type(self).__name__}._build__calculate_interest_rate has not been defined"
        )

    @staticmethod
    # @_decimal(round_to=2)
    def _build__calculate_fixed_periodic_repayment(
        loan_amount: Decimal,
        interest_rate: Decimal,
        **kwargs,  # To allow other arguments to be passed in without breaking the interface
    ) -> Decimal:
        """
        Calculate the period repayment, :math:`P`.

        This uses the loan amount (:math:`L`) and the interest rate (:math:`R`).

        The period repayment value, :math:`P`, for an interest-only loan is the
        same as the periodic interest so that:

        ..  math::

            P = LR

        In this case, the final repayment is then :math:`P + L`.
        """
        return loan_amount * interest_rate

    @staticmethod
    # @_decimal()
    def _build__calculate_total_repayments(
        total_repayments: int,
        **kwargs,  # To allow other arguments to be passed in without breaking the interface
    ) -> int:
        """
        Calculate the total repayments, :math:`N`.

        Note, however, that an interest-only loan can have as many repayments as
        the customer likes since the balance remains the same after each
        repayment. There is nothing to calculate here.
        """
        if total_repayments is None:
            # TODO: Consider adding this capture somewhere else
            raise ValueError(
                "The total repayments must be supplied for an interest-only loan."
            )

        return total_repayments

    # @_decimal(round_to=2)
    def calculate_balance_at_period(self, period: Decimal) -> Decimal:
        """
        Calculate the loan balance, :math:`B_{n}`, at the end of period
        :math:`n`.

        The balance at the end of period :math:`n`, :math:`b_{n}`, for an
        interest-only loan is:

        ..  math::

            B_{n} = L,  n < N

            B_{n} = 0,  n = N
        """
        return Decimal(0) if period == self.total_repayments else self.loan_amount

    # @_decimal(round_to=2)
    def calculate_repayment_principal_at_period(self, period: int) -> Decimal:
        """"""
        raise NotImplementedError(
            f"{type(self).__name__}.calculate_repayment_principal_at_period has not been defined"
        )

    # @_decimal(round_to=2)
    def calculate_repayment_interest_at_period(self, period: int) -> Decimal:
        """"""
        raise NotImplementedError(
            f"{type(self).__name__}.calculate_repayment_interest_at_period has not been defined"
        )

    # @_decimal(round_to=2)
    def calculate_cumulative_interest(self, period: int) -> Decimal:
        """
        Calculate the cumulative interest accrued at the end of period
        :math:`n`.

        The cumulative interest accrued at the end of period :math:`n` for a
        interest-only loan is:

        ..  math::

            I_{n} = TODO: formula here, also decide on notation for this (\\sum I_{k} or I_{n})
        """
