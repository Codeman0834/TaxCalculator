#!/usr/bin/env python3
"""Simple tax calculator with configurable brackets."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Bracket:
    threshold: float
    rate: float


DEFAULT_CONFIG = {
    "standard_deductions": {
        "single": 13_850,
        "married": 27_700,
    },
    "brackets": {
        "single": [
            {"threshold": 0, "rate": 0.10},
            {"threshold": 11_000, "rate": 0.12},
            {"threshold": 44_725, "rate": 0.22},
            {"threshold": 95_375, "rate": 0.24},
            {"threshold": 182_100, "rate": 0.32},
            {"threshold": 231_250, "rate": 0.35},
            {"threshold": 578_125, "rate": 0.37},
        ],
        "married": [
            {"threshold": 0, "rate": 0.10},
            {"threshold": 22_000, "rate": 0.12},
            {"threshold": 89_450, "rate": 0.22},
            {"threshold": 190_750, "rate": 0.24},
            {"threshold": 364_200, "rate": 0.32},
            {"threshold": 462_500, "rate": 0.35},
            {"threshold": 693_750, "rate": 0.37},
        ],
    },
}


def load_config(path: Path | None) -> dict:
    if path is None:
        return DEFAULT_CONFIG
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_brackets(raw_brackets: Iterable[dict]) -> list[Bracket]:
    brackets = [Bracket(float(item["threshold"]), float(item["rate"])) for item in raw_brackets]
    return sorted(brackets, key=lambda bracket: bracket.threshold)


def calculate_tax(taxable_income: float, brackets: Iterable[Bracket]) -> float:
    if taxable_income <= 0:
        return 0.0

    ordered = list(sorted(brackets, key=lambda bracket: bracket.threshold))
    tax = 0.0
    for index, bracket in enumerate(ordered):
        next_threshold = (
            ordered[index + 1].threshold if index + 1 < len(ordered) else taxable_income
        )
        upper_bound = min(taxable_income, next_threshold)
        if upper_bound <= bracket.threshold:
            break
        taxed_amount = upper_bound - bracket.threshold
        tax += taxed_amount * bracket.rate
        if upper_bound == taxable_income:
            break
    return tax


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Calculate estimated income tax.")
    parser.add_argument("income", type=float, help="Annual income before deductions")
    parser.add_argument(
        "--status",
        choices=("single", "married"),
        default="single",
        help="Filing status (default: single)",
    )
    parser.add_argument(
        "--standard-deduction",
        type=float,
        default=None,
        help="Override standard deduction amount",
    )
    parser.add_argument(
        "--brackets-file",
        type=Path,
        help="Optional JSON file with brackets and deductions",
    )
    parser.add_argument(
        "--round",
        type=int,
        default=2,
        help="Number of decimals to round outputs",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    config = load_config(args.brackets_file)
    deductions = config.get("standard_deductions", {})
    brackets_raw = config.get("brackets", {})

    if args.status not in brackets_raw:
        parser.error(f"No brackets found for status '{args.status}'.")

    deduction = (
        args.standard_deduction
        if args.standard_deduction is not None
        else float(deductions.get(args.status, 0))
    )

    taxable_income = max(0.0, args.income - deduction)
    brackets = parse_brackets(brackets_raw[args.status])
    tax = calculate_tax(taxable_income, brackets)
    effective_rate = 0.0 if args.income <= 0 else tax / args.income

    rounded = args.round
    print("Tax calculation summary")
    print("-----------------------")
    print(f"Filing status: {args.status}")
    print(f"Gross income: ${args.income:,.{rounded}f}")
    print(f"Standard deduction: ${deduction:,.{rounded}f}")
    print(f"Taxable income: ${taxable_income:,.{rounded}f}")
    print(f"Estimated tax: ${tax:,.{rounded}f}")
    print(f"Effective tax rate: {effective_rate:.{rounded}%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
