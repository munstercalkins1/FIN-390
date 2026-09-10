"""Five-year FCFF discounted cash flow model (all monetary inputs in USD millions)."""

# Editable inputs -- Nike FY2026 case; monetary inputs are USD millions.
starting_fcff = 2144.15
growth_rates = [0.03, 0.05, 0.06, 0.05, 0.04]
wacc = 0.10
terminal_growth = 0.03
non_operating_cash = 9027.0
debt = 7942.0
diluted_shares = 1481.0

# Editable sensitivity and reverse-DCF inputs
sensitivity_wacc_values = [0.09, 0.10, 0.11]
sensitivity_terminal_growth_values = [0.02, 0.03, 0.04]
target_share_price = 37.35
reverse_lower_shift = -0.05
reverse_upper_shift = 0.20


def calculate_value_per_share(
    fcff_start,
    yearly_growth_rates,
    discount_rate,
    perpetual_growth_rate,
    cash,
    total_debt,
    share_count,
):
    """Return DCF results using annual end-of-year FCFF, in USD millions."""
    if perpetual_growth_rate >= discount_rate:
        raise ValueError("Terminal growth must be less than WACC.")

    projected_fcff = []
    fcff = fcff_start
    for growth_rate in yearly_growth_rates:
        fcff *= 1 + growth_rate
        projected_fcff.append(fcff)

    explicit_pv = sum(
        fcff_value / (1 + discount_rate) ** year
        for year, fcff_value in enumerate(projected_fcff, start=1)
    )
    terminal_value = (
        projected_fcff[-1] * (1 + perpetual_growth_rate)
        / (discount_rate - perpetual_growth_rate)
    )
    terminal_pv = terminal_value / (1 + discount_rate) ** len(projected_fcff)
    enterprise_value = explicit_pv + terminal_pv
    equity_value = enterprise_value + cash - total_debt

    return {
        "fcff_values": projected_fcff,
        "present_value_explicit_fcff": explicit_pv,
        "terminal_value_year_5": terminal_value,
        "present_value_terminal_value": terminal_pv,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_diluted_share": equity_value / share_count,
        "terminal_value_share_of_enterprise_value": terminal_pv / enterprise_value,
    }


def print_sensitivity_grid():
    print("\nSensitivity Grid: Value per Diluted Share")
    header = "WACC \\ Terminal Growth" + "".join(
        f" | {terminal_growth_rate:.2%}"
        for terminal_growth_rate in sensitivity_terminal_growth_values
    )
    print(header)
    print("-" * len(header))

    for discount_rate in sensitivity_wacc_values:
        cells = []
        for perpetual_growth_rate in sensitivity_terminal_growth_values:
            if perpetual_growth_rate >= discount_rate:
                cells.append("invalid")
            else:
                result = calculate_value_per_share(
                    starting_fcff,
                    growth_rates,
                    discount_rate,
                    perpetual_growth_rate,
                    non_operating_cash,
                    debt,
                    diluted_shares,
                )
                cells.append(f"{result['value_per_diluted_share']:.4f}")
        print(f"{discount_rate:.2%}" + "".join(f" | {cell}" for cell in cells))


def solve_reverse_dcf_shift():
    if reverse_lower_shift >= reverse_upper_shift:
        print("\nReverse DCF: no solution; lower bound must be less than upper bound.")
        return
    if any(
        growth_rate + bound <= -1
        for growth_rate in growth_rates
        for bound in (reverse_lower_shift, reverse_upper_shift)
    ):
        print(
            "\nReverse DCF: no solution; the selected bracket pushes an annual "
            "growth rate to -100% or below."
        )
        return

    def price_for_shift(shift):
        shifted_growth_rates = [growth_rate + shift for growth_rate in growth_rates]
        return calculate_value_per_share(
            starting_fcff,
            shifted_growth_rates,
            wacc,
            terminal_growth,
            non_operating_cash,
            debt,
            diluted_shares,
        )["value_per_diluted_share"]

    lower_price = price_for_shift(reverse_lower_shift)
    upper_price = price_for_shift(reverse_upper_shift)
    minimum_price = min(lower_price, upper_price)
    maximum_price = max(lower_price, upper_price)

    print("\nReverse DCF: Uniform Shift to All Five Explicit Growth Rates")
    print(f"Target Share Price: {target_share_price:.4f}")
    print(
        "Held Fixed: starting FCFF, WACC, terminal growth, non-operating cash, "
        "debt, diluted shares, and five-year forecast length"
    )
    print(
        "Search Bounds: "
        f"{reverse_lower_shift:+.2%} to {reverse_upper_shift:+.2%}"
    )

    if not minimum_price <= target_share_price <= maximum_price:
        print("Solved Uniform Growth Shift: no solution in this bracket")
        return

    lower = reverse_lower_shift
    upper = reverse_upper_shift
    for _ in range(100):
        midpoint = (lower + upper) / 2
        midpoint_price = price_for_shift(midpoint)
        if abs(midpoint_price - target_share_price) < 1e-10:
            break
        if (lower_price - target_share_price) * (midpoint_price - target_share_price) <= 0:
            upper = midpoint
            upper_price = midpoint_price
        else:
            lower = midpoint
            lower_price = midpoint_price

    print(f"Solved Uniform Growth Shift: {midpoint:+.4%}")


def main():
    if len(growth_rates) != 5:
        raise ValueError("Exactly five yearly growth rates are required.")
    if terminal_growth >= wacc:
        raise ValueError(
            "Terminal growth must be less than WACC to calculate a Gordon-growth terminal value."
        )
    if diluted_shares <= 0:
        raise ValueError("Diluted shares must be greater than zero.")

    results = calculate_value_per_share(
        starting_fcff,
        growth_rates,
        wacc,
        terminal_growth,
        non_operating_cash,
        debt,
        diluted_shares,
    )

    for year, fcff_value in enumerate(results["fcff_values"], start=1):
        print(f"FCFF Year {year}: {fcff_value:.4f}")
    print(f"Present Value of Explicit FCFF: {results['present_value_explicit_fcff']:.4f}")
    print(f"Terminal Value at Year 5: {results['terminal_value_year_5']:.4f}")
    print(f"Present Value of Terminal Value: {results['present_value_terminal_value']:.4f}")
    print(f"Enterprise Value: {results['enterprise_value']:.4f}")
    print(f"Equity Value: {results['equity_value']:.4f}")
    print(f"Value per Diluted Share: {results['value_per_diluted_share']:.4f}")
    print(
        "Present Value of Terminal Value as Share of Enterprise Value: "
        f"{results['terminal_value_share_of_enterprise_value']:.4f}"
    )
    print_sensitivity_grid()
    solve_reverse_dcf_shift()


if __name__ == "__main__":
    main()
