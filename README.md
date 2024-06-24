<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![tests](https://github.com/Bilbottom/loan-calcs/actions/workflows/tests.yaml/badge.svg)](https://github.com/Bilbottom/loan-calcs/actions/workflows/tests.yaml)
[![coverage](coverage.svg)](https://github.com/dbrgn/coverage-badge)
[![GitHub last commit](https://img.shields.io/github/last-commit/Bilbottom/loan-calcs)](https://shields.io/badges/git-hub-last-commit)

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Bilbottom/loan-calcs/main.svg)](https://results.pre-commit.ci/latest/github/Bilbottom/loan-calcs/main)
[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)

</div>

---

# Loan Calculations

Library for common loan calculations.

## Notation

A _loan_ is a fixed value of money borrowed by an entity and usually repaid over a series of instalments.

The following notation is used throughout this project for loans:

- `L`: Loan amount
- `R`: Periodic interest rate
- `N`: Total number of repayments
- `P_n`: Total periodic repayment value at period `n`
- `P_{P, n}`: The principal part of the periodic repayment value at period `n`
- `P_{I, n}`: The interest part of the periodic repayment value at period `n`
- `b`: Whether the interest is applied before or after the repayment
- `B_n`: The balance on the loan at period `n`

The repayment for a loan, `P_n`, is split into two parts:

- The _principal_ part, `P_{P, n}`, which is paying off the original money that was borrowed.
- The _interest_ part, `P_{I, n}`, which is paying off the interest applied on the loan.

In 'real life', a loan can have other components such as fees. These are outside the scope of this project.

## Calculations

Many of the properties are calculated analytically. The calculations are described in the [`tex/proofs.pdf`](tex/proofs.pdf) file.
