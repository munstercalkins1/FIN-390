"""NIKE, Inc. five-year three-statement FCFF valuation application.

All currency figures are USD millions except per-share data.  This is an
educational model, not investment advice.  Run with Python 3.10+:

    python nike_fcff_application.py

The model intentionally keeps facts, forecast judgments, and outputs in
separate sections.  It writes a readable result file, `nike_fcff_output.md`,
so a reviewer can inspect the key results without rerunning the program.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import sys


YEARS = (2027, 2028, 2029, 2030, 2031)
VALUATION_DATE = "2026-09-10"
MARKET_PRICE = 36.62  # Regular-session close; see SOURCE_MAP.md.
SHARES_DILUTED = 1_481.0  # FY2026 diluted weighted-average shares.

# FY2026 audited opening balance sheet.  Source: NIKE FY2026 Form 10-K, p. 57.
OPENING = {
    "cash": 7_563.0,
    "short_investments": 1_464.0,
    "receivables": 5_931.0,
    "inventory": 7_501.0,
    "ppe": 4_796.0,
    "other_assets": 11_155.0,
    "payables": 3_600.0,
    "debt": 7_942.0,
    "other_liabilities": 12_003.0,
    "equity": 14_865.0,
}


@dataclass(frozen=True)
class Assumptions:
    """Forecast judgments.  Values are documented in ASSUMPTION_REGISTER.md."""

    wholesale_growth: tuple[float, ...] = (0.045, 0.050, 0.048, 0.045, 0.035)
    direct_growth: tuple[float, ...] = (0.000, 0.015, 0.030, 0.035, 0.025)
    other_growth: tuple[float, ...] = (-0.044, 0.000, 0.000, 0.000, 0.000)
    gross_margin: tuple[float, ...] = (0.435, 0.440, 0.445, 0.450, 0.450)
    sga_to_revenue: tuple[float, ...] = (0.340, 0.337, 0.334, 0.332, 0.332)
    cash_tax_rate: float = 0.203
    inventory_days: float = 103.4
    capex_to_revenue: float = 0.0147
    depreciation_to_opening_ppe: float = 747.0 / 4_796.0
    receivables_to_revenue: float = 5_931.0 / 46_398.0
    payables_to_cogs: float = 3_600.0 / 26_487.0
    other_assets_to_revenue: float = 11_155.0 / 46_398.0
    other_liabilities_to_revenue: float = 12_003.0 / 46_398.0
    stock_compensation: float = 715.0
    dividends: float = 2_450.0
    buybacks: float = 150.0
    annual_debt_repayment: float = 400.0
    other_income_to_revenue: float = 103.0 / 46_398.0
    wacc: float = 0.090
    terminal_growth: float = 0.025


BASE = Assumptions()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_assumptions(a: Assumptions) -> None:
    for label, path in (
        ("wholesale growth", a.wholesale_growth),
        ("direct growth", a.direct_growth),
        ("other growth", a.other_growth),
        ("gross margin", a.gross_margin),
        ("SG&A / revenue", a.sga_to_revenue),
    ):
        require(len(path) == len(YEARS), f"{label} must have exactly five annual values.")
    require(0 < a.wacc < 1, "WACC must be between 0% and 100%.")
    require(0 <= a.terminal_growth < a.wacc, "Terminal growth must be nonnegative and below WACC.")
    require(SHARES_DILUTED > 0, "Diluted shares must be positive.")


def project(a: Assumptions = BASE) -> list[dict[str, float]]:
    """Build linked income statement, balance sheet, cash flow, and FCFF."""
    validate_assumptions(a)
    opening = OPENING.copy()
    wholesale_weight = 27_453.0 / 46_398.0
    direct_weight = 17_720.0 / 46_398.0
    other_weight = 1.0 - wholesale_weight - direct_weight
    revenue = 46_398.0
    rows: list[dict[str, float]] = []

    for i, year in enumerate(YEARS):
        growth = (
            wholesale_weight * a.wholesale_growth[i]
            + direct_weight * a.direct_growth[i]
            + other_weight * a.other_growth[i]
        )
        revenue *= 1.0 + growth
        gross_profit = revenue * a.gross_margin[i]
        cogs = revenue - gross_profit
        sga = revenue * a.sga_to_revenue[i]  # Includes depreciation, consistent with reported presentation.
        ebit = gross_profit - sga
        depreciation = opening["ppe"] * a.depreciation_to_opening_ppe
        capex = revenue * a.capex_to_revenue
        other_income = revenue * a.other_income_to_revenue
        debt = max(0.0, opening["debt"] - a.annual_debt_repayment)
        debt_change = debt - opening["debt"]
        pretax_income = ebit + other_income
        tax = max(0.0, pretax_income) * a.cash_tax_rate
        net_income = pretax_income - tax

        receivables = revenue * a.receivables_to_revenue
        inventory = cogs * a.inventory_days / 365.0
        payables = cogs * a.payables_to_cogs
        other_assets = revenue * a.other_assets_to_revenue
        other_liabilities = revenue * a.other_liabilities_to_revenue
        ppe = opening["ppe"] + capex - depreciation

        delta_nwc = (
            (receivables - opening["receivables"])
            + (inventory - opening["inventory"])
            + (other_assets - opening["other_assets"])
            - (payables - opening["payables"])
            - (other_liabilities - opening["other_liabilities"])
        )
        cfo = net_income + depreciation + a.stock_compensation - delta_nwc
        cash_change = cfo - capex + debt_change - a.dividends - a.buybacks
        cash = opening["cash"] + cash_change
        equity = opening["equity"] + net_income + a.stock_compensation - a.dividends - a.buybacks
        nopat = ebit * (1.0 - a.cash_tax_rate)
        fcff = nopat + depreciation - capex - delta_nwc

        assets = cash + opening["short_investments"] + receivables + inventory + ppe + other_assets
        liabilities = payables + debt + other_liabilities
        row = {
            "year": float(year), "growth": growth, "revenue": revenue,
            "gross_profit": gross_profit, "cogs": cogs, "sga": sga, "ebit": ebit,
            "other_income": other_income, "pretax_income": pretax_income, "tax": tax,
            "net_income": net_income, "depreciation": depreciation, "capex": capex,
            "receivables": receivables, "inventory": inventory, "ppe": ppe,
            "other_assets": other_assets, "cash": cash, "payables": payables,
            "debt": debt, "other_liabilities": other_liabilities, "equity": equity,
            "assets": assets, "liabilities": liabilities, "liabilities_and_equity": liabilities + equity,
            "delta_nwc": delta_nwc, "cfo": cfo, "debt_change": debt_change, "cash_change": cash_change,
            "nopat": nopat, "fcff": fcff,
        }
        check_articulation(row, opening)
        rows.append(row)
        opening = {**row, "short_investments": opening["short_investments"]}
    return rows


def check_articulation(row: dict[str, float], opening: dict[str, float]) -> None:
    """Fail loudly on balance-sheet or cash-flow articulation errors."""
    balance_gap = row["assets"] - row["liabilities_and_equity"]
    require(abs(balance_gap) < 0.01, f"FY{row['year']:.0f} balance sheet gap: {balance_gap:.4f}")
    cash_from_bs = row["cash"] - opening["cash"]
    require(abs(cash_from_bs - row["cash_change"]) < 0.01,
            f"FY{row['year']:.0f} cash-flow-to-cash tie failed.")
    require(row["fcff"] > -50_000, f"FY{row['year']:.0f} FCFF sanity check failed.")


def dcf(rows: list[dict[str, float]], a: Assumptions = BASE) -> dict[str, float]:
    """Discount annual end-of-year FCFF and bridge enterprise value to equity."""
    validate_assumptions(a)
    pv_explicit = sum(row["fcff"] / (1.0 + a.wacc) ** (i + 1) for i, row in enumerate(rows))
    terminal_value = rows[-1]["fcff"] * (1.0 + a.terminal_growth) / (a.wacc - a.terminal_growth)
    pv_terminal = terminal_value / (1.0 + a.wacc) ** len(rows)
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + OPENING["cash"] + OPENING["short_investments"] - OPENING["debt"]
    return {
        "pv_explicit": pv_explicit, "terminal_value": terminal_value, "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value, "equity_value": equity_value,
        "per_share": equity_value / SHARES_DILUTED,
        "terminal_value_share": pv_terminal / enterprise_value,
    }


def run_case(name: str, a: Assumptions) -> dict[str, float | str]:
    rows = project(a)
    valuation = dcf(rows, a)
    return {"name": name, "fy31_revenue": rows[-1]["revenue"], "fy31_ebit": rows[-1]["ebit"], **valuation}


def scenario_cases() -> list[dict[str, float | str]]:
    """Causal cases; each is a coherent operating/valuation view, not a probability."""
    low = replace(
        BASE,
        wholesale_growth=(0.015, 0.025, 0.030, 0.030, 0.025),
        direct_growth=(-0.040, -0.020, 0.000, 0.010, 0.015),
        gross_margin=(0.425, 0.428, 0.432, 0.435, 0.435),
        sga_to_revenue=(0.345, 0.343, 0.340, 0.338, 0.338),
        wacc=0.100, terminal_growth=0.020,
    )
    high = replace(
        BASE,
        wholesale_growth=(0.060, 0.060, 0.055, 0.050, 0.040),
        direct_growth=(0.025, 0.045, 0.055, 0.050, 0.035),
        gross_margin=(0.440, 0.450, 0.458, 0.462, 0.462),
        sga_to_revenue=(0.337, 0.330, 0.325, 0.322, 0.322),
        wacc=0.085, terminal_growth=0.0275,
    )
    return [run_case("Downside", low), run_case("Base", BASE), run_case("Upside", high)]


def sensitivity() -> list[list[float | str]]:
    grid: list[list[float | str]] = []
    for wacc in (0.080, 0.090, 0.100):
        for growth in (0.020, 0.025, 0.030):
            scenario = replace(BASE, wacc=wacc, terminal_growth=growth)
            grid.append([wacc, growth, dcf(project(scenario), scenario)["per_share"]])
    return grid


def reverse_dcf() -> float:
    """Solve for an equal shift to every explicit Direct-growth rate at the market price."""
    # The low bound deliberately permits a severe contraction because the
    # observed market price is below the value produced by a merely slow
    # recovery.  The resulting shift is an implied stress condition, not a
    # plausible base forecast.
    lower, upper = -0.30, 0.20
    def price(shift: float) -> float:
        a = replace(BASE, direct_growth=tuple(value + shift for value in BASE.direct_growth))
        return dcf(project(a), a)["per_share"]
    require(price(lower) <= MARKET_PRICE <= price(upper), "Market price is outside reverse-DCF search bracket.")
    for _ in range(100):
        midpoint = (lower + upper) / 2.0
        if price(midpoint) < MARKET_PRICE:
            lower = midpoint
        else:
            upper = midpoint
    return (lower + upper) / 2.0


def validation() -> list[str]:
    """Known-answer, direction, boundary, bridge, and base-year reconciliation checks."""
    rows = project(BASE)
    base_assets = sum(OPENING[key] for key in ("cash", "short_investments", "receivables", "inventory", "ppe", "other_assets"))
    base_claims = OPENING["payables"] + OPENING["debt"] + OPENING["other_liabilities"] + OPENING["equity"]
    require(abs(base_assets - base_claims) < 0.01, "FY2026 filing opening balance sheet does not reconcile.")
    # Synthetic known-answer: 100 FCFF next year, WACC 10%, g 0%, five years.
    synthetic_rows = [{"fcff": 100.0} for _ in range(5)]
    synthetic = dcf(synthetic_rows, replace(BASE, wacc=0.10, terminal_growth=0.0))
    expected_ev = sum(100.0 / 1.1 ** year for year in range(1, 6)) + (100.0 / 0.10) / 1.1 ** 5
    require(abs(synthetic["enterprise_value"] - expected_ev) < 0.0001, "Synthetic DCF known-answer failed.")
    low_wacc = dcf(rows, replace(BASE, wacc=0.080))
    high_wacc = dcf(rows, replace(BASE, wacc=0.100))
    require(low_wacc["per_share"] > high_wacc["per_share"], "WACC monotonicity failed.")
    low_g = dcf(rows, replace(BASE, terminal_growth=0.020))
    high_g = dcf(rows, replace(BASE, terminal_growth=0.030))
    require(low_g["per_share"] < high_g["per_share"], "Terminal-growth monotonicity failed.")
    value = dcf(rows)
    require(abs(value["equity_value"] - (value["enterprise_value"] + OPENING["cash"] + OPENING["short_investments"] - OPENING["debt"])) < 0.01,
            "Enterprise-to-equity bridge failed.")
    return [
        "PASS — FY2026 opening balance sheet reconciles to assets = liabilities + equity.",
        "PASS — synthetic known-answer DCF reconciliation.",
        "PASS — WACC and terminal-growth monotonicity checks.",
        "PASS — enterprise-to-equity bridge arithmetic.",
        "PASS — every forecast balance sheet and cash-flow-to-cash tie.",
    ]


def money(value: float) -> str:
    return f"${value:,.1f}"


def output_markdown() -> str:
    rows, base = project(BASE), dcf(project(BASE), BASE)
    checks, cases, grid = validation(), scenario_cases(), sensitivity()
    reverse_shift = reverse_dcf()
    lines = [
        "# NIKE FCFF Valuation — Visible Output",
        "",
        f"Valuation date: {VALUATION_DATE}. Currency: USD millions except per-share data. Share basis: FY2026 diluted weighted-average shares ({SHARES_DILUTED:,.1f}m).",
        "",
        "## Base-case DCF and bridge",
        "",
        f"- Enterprise value: {money(base['enterprise_value'])}",
        f"- Plus cash and short-term investments: {money(OPENING['cash'] + OPENING['short_investments'])}",
        f"- Less total debt: {money(OPENING['debt'])}",
        f"- Equity value: {money(base['equity_value'])}",
        f"- Base intrinsic value: **${base['per_share']:.2f} per share**",
        f"- Market reference: ${MARKET_PRICE:.2f}; terminal value is {base['terminal_value_share']:.1%} of enterprise value.",
        "",
        "## Five-year FCFF forecast",
        "",
        "| FY | Revenue | EBIT | NOPAT | FCFF | Balance-sheet gap |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['year']:.0f}E | {money(row['revenue'])} | {money(row['ebit'])} | {money(row['nopat'])} | {money(row['fcff'])} | {row['assets'] - row['liabilities_and_equity']:.2f} |")
    lines += [
        "", "## Five-year income statement", "",
        "| USD millions | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for label, key in (("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"), ("EBIT", "ebit"), ("Tax", "tax"), ("Net income", "net_income")):
        lines.append(f"| {label} |" + "|".join(money(row[key]) for row in rows) + "|")
    lines += [
        "", "## Five-year balance sheet", "",
        "| USD millions | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for label, key in (("Cash", "cash"), ("Receivables", "receivables"), ("Inventory", "inventory"), ("PP&E", "ppe"), ("Other assets", "other_assets"), ("Assets", "assets"), ("Payables", "payables"), ("Debt", "debt"), ("Other liabilities", "other_liabilities"), ("Equity", "equity"), ("Liabilities + equity", "liabilities_and_equity")):
        lines.append(f"| {label} |" + "|".join(money(row[key]) for row in rows) + "|")
    lines += [
        "", "## Five-year cash flow and FCFF", "",
        "| USD millions | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for label, key in (("Net income", "net_income"), ("Depreciation", "depreciation"), ("Stock compensation", "stock_compensation"), ("Change in NWC", "delta_nwc"), ("Cash from operations", "cfo"), ("Capital expenditures", "capex"), ("Debt change", "debt_change"), ("Dividends", "dividends"), ("Buybacks", "buybacks"), ("Cash change", "cash_change"), ("FCFF", "fcff")):
        if key in ("stock_compensation", "dividends", "buybacks"):
            values = [getattr(BASE, key) for _ in rows]
        else:
            values = [row[key] for row in rows]
        lines.append(f"| {label} |" + "|".join(money(value) for value in values) + "|")
    lines += ["", "## Causal valuation cases", "", "| Case | FY2031 revenue | FY2031 EBIT | Value / share |", "|---|---:|---:|---:|"]
    for case in cases:
        lines.append(f"| {case['name']} | {money(float(case['fy31_revenue']))} | {money(float(case['fy31_ebit']))} | ${float(case['per_share']):.2f} |")
    lines += ["", "Decision range: downside to upside case, not a probability-weighted target.", "", "## WACC–terminal-growth sensitivity", "", "| WACC | Terminal growth | Value / share |", "|---:|---:|---:|"]
    for wacc, growth, per_share in grid:
        lines.append(f"| {float(wacc):.1%} | {float(growth):.1%} | ${float(per_share):.2f} |")
    lines += [
        "", "## Reverse DCF", "",
        f"Holding all base inputs except the five Direct-growth rates constant, the ${MARKET_PRICE:.2f} market reference implies an equal annual Direct-growth shift of {reverse_shift:+.2%}. This is a model-implied condition, not a forecast.",
        "", "## Validation results", "",
    ]
    lines.extend(f"- {item}" for item in checks)
    return "\n".join(lines) + "\n"


def main() -> None:
    if "--failure-test" in sys.argv:
        # Highest-risk failure test: a cash-balance edit that is not reflected
        # in the cash-flow statement must be detected rather than silently used.
        corrupted = project(BASE)[0].copy()
        corrupted["cash"] += 1.0
        try:
            check_articulation(corrupted, OPENING)
        except ValueError as error:
            print(f"PASS — expected fail-loud articulation error: {error}")
            return
        raise RuntimeError("Failure test did not detect corrupted cash.")
    report = output_markdown()
    Path("nike_fcff_output.md").write_text(report, encoding="utf-8")
    print(report)
    print("Wrote nike_fcff_output.md")


if __name__ == "__main__":
    main()
