"""Deterministic three-investor checks and printed-number-only memos."""
from __future__ import annotations

from typing import Any

Audit = dict[str, Any]


def status_all(rows: list[dict[str, Any]], left: str, right: str | None = None, minimum: float | None = None) -> str:
    """Return pass/fail/not known without estimating a missing input."""
    left_values = [row[left]["value"] for row in rows]
    right_values = [row[right]["value"] for row in rows] if right else []
    if any(value is None for value in left_values + right_values):
        return "not known"
    if minimum is not None:
        return "pass" if all(value >= minimum for value in left_values) else "fail"
    return "pass" if all(a >= b for a, b in zip(left_values, right_values)) else "fail"


def growing(rows: list[dict[str, Any]], key: str) -> str:
    values = [row[key]["value"] for row in rows]
    if any(value is None for value in values):
        return "not known"
    return "pass" if values[-1] > values[0] else "fail"


def latest_at_least(rows: list[dict[str, Any]], key: str, threshold: float) -> str:
    value = rows[-1][key]["value"]
    return "not known" if value is None else ("pass" if value >= threshold else "fail")


def latest_at_most(rows: list[dict[str, Any]], key: str, threshold: float) -> str:
    value = rows[-1][key]["value"]
    return "not known" if value is None else ("pass" if value <= threshold else "fail")


def checks(audit: Audit, graham_ratio_threshold: float = 2.0) -> list[dict[str, str]]:
    rows = audit["rows"]
    return [
        {"Investor": "Buffett", "Check": "ROE of 15% or more every year", "Result": status_all(rows, "roe", minimum=15)},
        {"Investor": "Buffett", "Check": "Owner earnings positive every year", "Result": status_all(rows, "owner_earnings", minimum=0.0000001)},
        {"Investor": "Buffett", "Check": "Owner earnings grew, first year to last", "Result": growing(rows, "owner_earnings")},
        {"Investor": "Graham", "Check": f"Current ratio of {graham_ratio_threshold:.1f} or more, latest year", "Result": latest_at_least(rows, "current_ratio", graham_ratio_threshold)},
        {"Investor": "Graham", "Check": "Net income positive every year", "Result": status_all(rows, "net_income", minimum=0.0000001)},
        {"Investor": "Graham", "Check": "Net income grew, first year to last", "Result": growing(rows, "net_income")},
        {"Investor": "Burry", "Check": "Operating cash flow at least net income every year", "Result": status_all(rows, "operating_cash_flow", "net_income")},
        {"Investor": "Burry", "Check": "Liabilities no more than twice equity, latest year", "Result": latest_at_most(rows, "liabilities_to_equity", 2.0)},
    ]


def verdict(check_rows: list[dict[str, str]], investor: str) -> str:
    outcomes = [row["Result"] for row in check_rows if row["Investor"] == investor]
    if "not known" in outcomes:
        return "no decision"
    return "pass" if "fail" not in outcomes else "watch"


def panel_verdicts(check_rows: list[dict[str, str]]) -> dict[str, str]:
    return {investor: verdict(check_rows, investor) for investor in ("Buffett", "Graham", "Burry")}


def number(value: float | None, suffix: str = "") -> str:
    return "not known" if value is None else f"{value:,.2f}{suffix}"


def memos(audit: Audit, graham_ratio_threshold: float) -> dict[str, str]:
    last = audit["rows"][-1]
    verdicts = panel_verdicts(checks(audit, graham_ratio_threshold))
    return {
        "Buffett": f"Verdict: {verdicts['Buffett']}. Latest ROE is {number(last['roe']['value'], '%')}; latest owner earnings are {number(last['owner_earnings']['value'])}. The table prints all three checks.",
        "Graham": f"Verdict: {verdicts['Graham']}. Latest current ratio is {number(last['current_ratio']['value'])}; latest net income is {number(last['net_income']['value'])}. The table prints all three checks.\n\nThreshold kept: {graham_ratio_threshold:.1f} — retain the stated Graham rule unless you intentionally change the screen design.",
        "Burry": f"Verdict: {verdicts['Burry']}. Latest operating cash flow is {number(last['operating_cash_flow']['value'])}; latest net income is {number(last['net_income']['value'])}; liabilities ÷ equity is {number(last['liabilities_to_equity']['value'])}. The table prints both checks.",
    }
