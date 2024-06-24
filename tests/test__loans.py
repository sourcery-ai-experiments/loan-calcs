"""
Unit tests for the ``src.main`` module.
"""

import decimal

import loan_calcs


def test__fixed_principal_loan(fixed_principal_loan: loan_calcs.FixedPrincipalLoan):
    """
    Test that a fixed principal loan is generated correctly.
    """
    repayment = decimal.Decimal("166.6666666666666666666666667")
    assert fixed_principal_loan.principal_repayment == repayment
    assert fixed_principal_loan.periodic_repayment == repayment


def test__fixed_repayment_loan(fixed_repayment_loan: loan_calcs.FixedRepaymentLoan):
    """
    Test that a fixed repayment loan is generated correctly.
    """
    assert fixed_repayment_loan.total_repayments == 15
