"""NIKE five-year pro-forma and FCFE valuation (USD millions except per-share data)."""

from __future__ import annotations

import sys


# FY2026 actual opening balance sheet.  Source: NIKE FY2026 Form 10-K, p. 57.
OPENING = {
    "revenue": 46_398.0, "cash": 7_563.0, "short_investments": 1_464.0,
    "receivables": 5_931.0, "inventory": 7_501.0, "ppe": 4_796.0,
    "other_assets": 11_155.0, "payables": 3_600.0, "debt": 7_942.0,
    "revolver": 0.0, "other_liabilities": 12_003.0, "equity": 14_865.0,
}

YEARS = (2027, 2028, 2029, 2030, 2031)

# The values and labels are documented in lab10_nike_proforma.md.
# NIKE-specific line: Direct/wholesale channel normalization. FY2026 Direct
# revenue fell while wholesale grew. These actual FY2026 channel weights and
# channel growth paths generate consolidated revenue growth below.
WHOLESALE_WEIGHT = 27_453.0 / 46_398.0
DIRECT_WEIGHT = 17_720.0 / 46_398.0
OTHER_REVENUE_WEIGHT = 1.0 - WHOLESALE_WEIGHT - DIRECT_WEIGHT
WHOLESALE_GROWTH = (0.045, 0.050, 0.048, 0.045, 0.035)
DIRECT_GROWTH = (0.000, 0.015, 0.030, 0.035, 0.025)
OTHER_REVENUE_GROWTH = (-0.044, 0.000, 0.000, 0.000, 0.000)
REVENUE_GROWTH = tuple(
    WHOLESALE_WEIGHT * wholesale + DIRECT_WEIGHT * direct + OTHER_REVENUE_WEIGHT * other
    for wholesale, direct, other in zip(WHOLESALE_GROWTH, DIRECT_GROWTH, OTHER_REVENUE_GROWTH)
)
# The same channel-normalization line then produces a gradual margin benefit,
# not a one-year jump back to the FY2024 margin.
FY2026_GROSS_MARGIN = 0.429
CHANNEL_MIX_MARGIN_RECOVERY = (0.006, 0.011, 0.016, 0.021, 0.021)
GROSS_MARGIN = tuple(FY2026_GROSS_MARGIN + x for x in CHANNEL_MIX_MARGIN_RECOVERY)
SGA_TO_GROSS_PROFIT = (0.790, 0.780, 0.770, 0.765, 0.765)
TAX_RATE = 0.203
INVENTORY_DAYS = 103.4
RECEIVABLES_TO_REVENUE = 5_931.0 / 46_398.0
PAYABLES_TO_COGS = 3_600.0 / 26_487.0
OTHER_ASSETS_TO_REVENUE = 11_155.0 / 46_398.0
OTHER_LIABILITIES_TO_REVENUE = 12_003.0 / 46_398.0
DEPRECIATION_TO_PPE = 747.0 / 4_796.0
CAPEX_TO_REVENUE = 684.0 / 46_398.0
STOCK_COMPENSATION = 715.0
DIVIDENDS = 2_450.0
BUYBACKS = 150.0
DEBT_REPAYMENT = 400.0
OTHER_INCOME_TO_REVENUE = 103.0 / 46_398.0
MINIMUM_CASH = 2_000.0
REVOLVER_RATE = 0.060
COST_OF_EQUITY = 0.090
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 1_481.0


def assert_balanced(year: int, row: dict[str, float]) -> None:
    gap = row["assets"] - row["liabilities"] - row["equity"]
    if abs(gap) > 0.05:
        raise ValueError(f"FY{year}E is not balanced: gap {gap:.1f}")
    if row["cash"] < MINIMUM_CASH - 0.05:
        raise ValueError(f"FY{year}E cash is below the floor: {row['cash']:.1f}")


def project() -> list[dict[str, float]]:
    opening = OPENING.copy()
    results: list[dict[str, float]] = []
    for i, year in enumerate(YEARS):
        revenue = opening["revenue"] * (1 + REVENUE_GROWTH[i])
        gross_profit = revenue * GROSS_MARGIN[i]
        cogs = revenue - gross_profit
        sga = gross_profit * SGA_TO_GROSS_PROFIT[i]
        operating_income = gross_profit - sga
        other_income = revenue * OTHER_INCOME_TO_REVENUE
        interest = opening["revolver"] * REVOLVER_RATE
        pretax_income = operating_income + other_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        inventory = cogs * INVENTORY_DAYS / 365.0
        receivables = revenue * RECEIVABLES_TO_REVENUE
        payables = cogs * PAYABLES_TO_COGS
        other_assets = revenue * OTHER_ASSETS_TO_REVENUE
        other_liabilities = revenue * OTHER_LIABILITIES_TO_REVENUE
        depreciation = opening["ppe"] * DEPRECIATION_TO_PPE
        capex = revenue * CAPEX_TO_REVENUE
        ppe = opening["ppe"] + capex - depreciation
        debt = max(0.0, opening["debt"] - DEBT_REPAYMENT)
        debt_change = debt - opening["debt"]

        fcfe = (net_income + depreciation + STOCK_COMPENSATION - capex
                - (inventory - opening["inventory"])
                - (receivables - opening["receivables"])
                - (other_assets - opening["other_assets"])
                + (payables - opening["payables"])
                + (other_liabilities - opening["other_liabilities"])
                + debt_change)
        cash_before_revolver = opening["cash"] + fcfe - DIVIDENDS - BUYBACKS
        revolver = opening["revolver"]
        if cash_before_revolver < MINIMUM_CASH:
            revolver += MINIMUM_CASH - cash_before_revolver
            cash = MINIMUM_CASH
        else:
            repayment = min(revolver, cash_before_revolver - MINIMUM_CASH)
            revolver -= repayment
            cash = cash_before_revolver - repayment
        equity = opening["equity"] + net_income + STOCK_COMPENSATION - DIVIDENDS - BUYBACKS
        assets = cash + opening["short_investments"] + receivables + inventory + ppe + other_assets
        liabilities = payables + debt + revolver + other_liabilities
        row = {"year": float(year), "revenue": revenue, "gross_profit": gross_profit,
               "sga": sga, "operating_income": operating_income, "other_income": other_income,
               "interest": interest, "pretax_income": pretax_income, "tax": tax,
               "net_income": net_income, "depreciation": depreciation, "capex": capex,
               "receivables": receivables, "inventory": inventory, "ppe": ppe,
               "other_assets": other_assets, "cash": cash, "payables": payables, "debt": debt,
               "revolver": revolver, "other_liabilities": other_liabilities, "equity": equity,
               "assets": assets, "liabilities": liabilities,
               "liabilities_and_equity": liabilities + equity, "fcfe": fcfe}
        assert_balanced(year, row)
        results.append(row)
        opening = {**row, "short_investments": opening["short_investments"]}
    return results


def print_table(title: str, rows: list[tuple[str, str]], results: list[dict[str, float]]) -> None:
    print(f"\n{title}")
    print(f"{'USD millions':<31}" + "".join(f"FY{int(r['year'])}E{'':>10}" for r in results))
    print("-" * 111)
    for label, key in rows:
        print(f"{label:<31}" + "".join(f"{r[key]:>16.1f}" for r in results))


def value_equity(results: list[dict[str, float]]) -> tuple[float, float]:
    explicit = sum(r["fcfe"] / (1 + COST_OF_EQUITY) ** (i + 1) for i, r in enumerate(results))
    terminal = results[-1]["fcfe"] * (1 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
    equity_value = explicit + terminal / (1 + COST_OF_EQUITY) ** len(results)
    return equity_value, equity_value / SHARES_OUTSTANDING


def main() -> None:
    results = project()
    if "--break" in sys.argv:
        # Deliberate test: do not use for the submitted base case.
        broken = results[0].copy()
        broken["cash"] += 1.0
        broken["assets"] += 1.0
        assert_balanced(int(broken["year"]), broken)
    print_table("Income Statement", [("Revenue", "revenue"), ("Gross profit", "gross_profit"),
        ("Selling & administrative", "sga"), ("Operating income", "operating_income"),
        ("Other income", "other_income"), ("Interest", "interest"), ("Pretax income", "pretax_income"),
        ("Tax", "tax"), ("Net income", "net_income")], results)
    print_table("Balance Sheet", [("Cash", "cash"), ("Receivables", "receivables"),
        ("Inventory", "inventory"), ("PP&E", "ppe"), ("Other assets", "other_assets"),
        ("Assets", "assets"), ("Payables", "payables"), ("Debt", "debt"),
        ("Revolver", "revolver"), ("Other liabilities", "other_liabilities"), ("Equity", "equity"),
        ("Liabilities + equity", "liabilities_and_equity")], results)
    print_table("Cash Flow / FCFE", [("Net income", "net_income"), ("Depreciation", "depreciation"),
        ("Capital spending", "capex"), ("Free cash flow to equity", "fcfe")], results)
    print("\nChecks")
    for r in results:
        print(f"FY{int(r['year'])}E: assets - liabilities - equity = "
              f"{r['assets'] - r['liabilities'] - r['equity']:.1f}; "
              f"cash at or above floor = {r['cash'] >= MINIMUM_CASH}")
    equity_value, per_share = value_equity(results)
    print("\nValuation")
    print(f"Equity value: ${equity_value:,.1f} million")
    print(f"Value per share: ${per_share:,.2f}")


if __name__ == "__main__":
    main()
