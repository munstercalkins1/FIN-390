"""ABG five-year pro-forma, three-statement model (USD millions)."""

from __future__ import annotations


# Opening balance sheet: FY2025, USD millions.
OPENING = {
    "revenue": 17_999.0,
    "inventory": 2_135.8,
    "ppe": 3_070.4,
    "other_assets": 6_371.6,
    "cash": 40.4,
    "floor_plan": 2_027.0,
    "term_debt": 3_572.0,
    "revolver": 0.0,
    "other_liabilities": 2_127.5,
    "equity": 3_891.7,
}

YEARS = (2026, 2027, 2028, 2029, 2030)

# Assumptions supplied in the Lab 09 instructions.
REVENUE_GROWTH = 0.018
GROSS_MARGIN = 0.1705
SGA_TO_GROSS_PROFIT = (0.665, 0.655, 0.645, 0.645, 0.645)
DEPRECIATION_TO_OPENING_PPE = 82.4 / 3_070.4
IMPAIRMENT = 120.0
CAPEX = 250.0
TAX_RATE = 0.255
INVENTORY_DAYS = 2_135.8 / (17_999.0 - 3_071.7) * 365
FLOOR_PLAN_TO_INVENTORY = 2_027.0 / 2_135.8
OTHER_WORKING_CAPITAL_RATE = 0.008
MINIMUM_CASH = 25.0
REVOLVER_LIMIT = 850.0
REVOLVER_RATE = 0.06
DEBT_REPAYMENT = 150.0
SHARE_BUYBACK = 150.0
FLOOR_PLAN_RATE = 0.0467
TERM_DEBT_RATE = 0.0544
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 17.951349


def assert_balanced(year: int, row: dict[str, float]) -> None:
    """Raise a clear error if the model's balance-sheet checks fail."""
    gap = row["assets"] - row["liabilities"] - row["equity"]
    if abs(gap) > 0.05:
        raise ValueError(f"FY{year}E is not balanced: gap {gap:.1f}")
    if row["cash"] < MINIMUM_CASH - 0.05:
        raise ValueError(
            f"FY{year}E cash is below the minimum: {row['cash']:.1f} vs {MINIMUM_CASH:.1f}"
        )


def project() -> list[dict[str, float]]:
    """Project the income statement, balance sheet, and FCFE from 2026–2030."""
    opening = OPENING.copy()
    results: list[dict[str, float]] = []

    for index, year in enumerate(YEARS):
        revenue = opening["revenue"] * (1 + REVENUE_GROWTH)
        gross_profit = revenue * GROSS_MARGIN
        sga = gross_profit * SGA_TO_GROSS_PROFIT[index]
        depreciation = opening["ppe"] * DEPRECIATION_TO_OPENING_PPE
        operating_income = gross_profit - sga - depreciation - IMPAIRMENT

        interest = (
            opening["floor_plan"] * FLOOR_PLAN_RATE
            + opening["term_debt"] * TERM_DEBT_RATE
            + opening["revolver"] * REVOLVER_RATE
        )
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365
        floor_plan = inventory * FLOOR_PLAN_TO_INVENTORY
        ppe = opening["ppe"] + CAPEX - depreciation
        change_revenue = revenue - opening["revenue"]
        other_working_capital = OTHER_WORKING_CAPITAL_RATE * change_revenue
        other_assets = opening["other_assets"] + other_working_capital - IMPAIRMENT
        term_debt = opening["term_debt"] - DEBT_REPAYMENT
        other_liabilities = opening["other_liabilities"]
        equity = opening["equity"] + net_income - SHARE_BUYBACK

        change_inventory = inventory - opening["inventory"]
        change_floor_plan = floor_plan - opening["floor_plan"]
        fcfe = (
            net_income
            + depreciation
            + IMPAIRMENT
            - CAPEX
            - change_inventory
            - other_working_capital
            + change_floor_plan
            - DEBT_REPAYMENT
        )

        cash_before_revolver = opening["cash"] + fcfe - SHARE_BUYBACK
        revolver = opening["revolver"]
        if cash_before_revolver < MINIMUM_CASH:
            draw = MINIMUM_CASH - cash_before_revolver
            revolver += draw
            if revolver > REVOLVER_LIMIT + 0.05:
                raise ValueError(
                    f"FY{year}E revolver requirement {revolver:.1f} exceeds limit {REVOLVER_LIMIT:.1f}"
                )
            cash = MINIMUM_CASH
        else:
            repayment = min(revolver, cash_before_revolver - MINIMUM_CASH)
            revolver -= repayment
            cash = cash_before_revolver - repayment

        assets = inventory + ppe + other_assets + cash
        liabilities = floor_plan + term_debt + revolver + other_liabilities
        row = {
            "year": float(year),
            "revenue": revenue,
            "gross_profit": gross_profit,
            "sga": sga,
            "depreciation": depreciation,
            "impairment": IMPAIRMENT,
            "operating_income": operating_income,
            "interest": interest,
            "pretax_income": pretax_income,
            "tax": tax,
            "net_income": net_income,
            "inventory": inventory,
            "ppe": ppe,
            "other_assets": other_assets,
            "cash": cash,
            "floor_plan": floor_plan,
            "term_debt": term_debt,
            "revolver": revolver,
            "other_liabilities": other_liabilities,
            "equity": equity,
            "assets": assets,
            "liabilities": liabilities,
            "liabilities_and_equity": liabilities + equity,
            "capex": CAPEX,
            "change_inventory": change_inventory,
            "change_floor_plan": change_floor_plan,
            "debt_repayment": DEBT_REPAYMENT,
            "other_working_capital": other_working_capital,
            "fcfe": fcfe,
        }
        assert_balanced(year, row)
        results.append(row)
        opening = {
            "revenue": revenue,
            "inventory": inventory,
            "ppe": ppe,
            "other_assets": other_assets,
            "cash": cash,
            "floor_plan": floor_plan,
            "term_debt": term_debt,
            "revolver": revolver,
            "other_liabilities": other_liabilities,
            "equity": equity,
        }

    return results


def print_table(title: str, rows: list[tuple[str, str]], results: list[dict[str, float]]) -> None:
    print(f"\n{title}")
    print(f"{'USD millions':<31}" + "".join(f"FY{int(row['year'])}E{'':>10}" for row in results))
    print("-" * 96)
    for label, key in rows:
        print(f"{label:<31}" + "".join(f"{row[key]:>16.1f}" for row in results))


def value_equity(results: list[dict[str, float]]) -> tuple[float, float, float]:
    explicit_value = sum(
        row["fcfe"] / (1 + COST_OF_EQUITY) ** (index + 1)
        for index, row in enumerate(results)
    )
    terminal_fcfe = results[-1]["fcfe"] + DEBT_REPAYMENT
    terminal_value = terminal_fcfe * (1 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
    terminal_present_value = terminal_value / (1 + COST_OF_EQUITY) ** len(results)
    equity_value = explicit_value + terminal_present_value
    terminal_share = terminal_present_value / equity_value
    return equity_value, terminal_share, equity_value / SHARES_OUTSTANDING


def main() -> None:
    results = project()
    print_table(
        "Income Statement",
        [
            ("Revenue", "revenue"),
            ("Gross profit", "gross_profit"),
            ("SG&A", "sga"),
            ("Depreciation", "depreciation"),
            ("Impairment", "impairment"),
            ("Operating income", "operating_income"),
            ("Interest", "interest"),
            ("Pretax income", "pretax_income"),
            ("Tax", "tax"),
            ("Net income", "net_income"),
        ],
        results,
    )
    print_table(
        "Balance Sheet",
        [
            ("Inventory", "inventory"),
            ("PP&E", "ppe"),
            ("Other assets", "other_assets"),
            ("Cash", "cash"),
            ("Assets", "assets"),
            ("Floor plan", "floor_plan"),
            ("Term debt", "term_debt"),
            ("Revolver", "revolver"),
            ("Other liabilities", "other_liabilities"),
            ("Equity", "equity"),
            ("Liabilities + equity", "liabilities_and_equity"),
        ],
        results,
    )
    print_table(
        "Cash Flow / FCFE",
        [
            ("Net income", "net_income"),
            ("Depreciation", "depreciation"),
            ("Impairment", "impairment"),
            ("Capital spending", "capex"),
            ("Change in inventory", "change_inventory"),
            ("Other working capital", "other_working_capital"),
            ("Change in floor plan", "change_floor_plan"),
            ("Debt repayment", "debt_repayment"),
            ("Free cash flow to equity", "fcfe"),
        ],
        results,
    )
    print("\nChecks")
    for row in results:
        gap = row["assets"] - row["liabilities"] - row["equity"]
        print(
            f"FY{int(row['year'])}E: assets - liabilities - equity = {gap:.1f}; "
            f"cash at or above minimum = {row['cash'] >= MINIMUM_CASH}"
        )

    equity_value, terminal_share, value_per_share = value_equity(results)
    print("\nValuation")
    print(f"Equity value: ${equity_value:,.1f} million")
    print(f"Share of value after 2030: {terminal_share:.1%}")
    print(f"Value per share: ${value_per_share:,.2f}")


if __name__ == "__main__":
    main()
