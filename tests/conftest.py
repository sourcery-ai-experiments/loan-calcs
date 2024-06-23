"""
Project-level fixtures.
"""

import pytest

import loan_calcs


@pytest.fixture
def fixed_principal_loan() -> loan_calcs.FixedPrincipalLoan:
    """
    Return a fixed principal loan object.
    """
    return loan_calcs.FixedPrincipalLoan.build(
        loan_amount=1000,
        interest_rate=0.05,
        total_repayments=6,
    )


@pytest.fixture
def fixed_repayment_loan() -> loan_calcs.FixedRepaymentLoan:
    """
    Return a fixed repayment loan object.
    """
    return loan_calcs.FixedRepaymentLoan.build(
        loan_amount=1000,
        interest_rate=0.05,
        fixed_periodic_repayment=100,
    )


@pytest.fixture
def interest_only_loan() -> loan_calcs.InterestOnlyLoan:
    """
    Return an interest-only loan object.
    """
    return loan_calcs.InterestOnlyLoan.build(
        loan_amount=1000,
        interest_rate=0.05,
        total_repayments=6,
    )
