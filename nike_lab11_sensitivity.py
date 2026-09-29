"""Lab 11 one-at-a-time sensitivity analysis for NIKE (USD millions except per share)."""

from __future__ import annotations

from nike_lab10_proforma import (
    CHANNEL_MIX_MARGIN_RECOVERY,
    DIRECT_GROWTH,
    YEARS,
    project,
    value_equity,
)

# Locked independent-input ranges.  Each tuple is FY2027E through FY2031E.
# Direct-growth cases move every annual Direct growth assumption by +/- 2.0 percentage points.
# Margin-recovery cases move every annual recovery assumption by +/- 100 basis points.
DIRECT_GROWTH_CASES = {
    "Lower": tuple(value - 0.020 for value in DIRECT_GROWTH),
    "Base": DIRECT_GROWTH,
    "Higher": tuple(value + 0.020 for value in DIRECT_GROWTH),
}
CHANNEL_MIX_MARGIN_RECOVERY_CASES = {
    "Lower": tuple(value - 0.010 for value in CHANNEL_MIX_MARGIN_RECOVERY),
    "Base": CHANNEL_MIX_MARGIN_RECOVERY,
    "Higher": tuple(value + 0.010 for value in CHANNEL_MIX_MARGIN_RECOVERY),
}


def check_summary(results: list[dict[str, float]]) -> str:
    """Return visible accounting-check evidence; project() already raises on a failure."""
    return "; ".join(
        f"FY{int(row['year'])}: gap={row['assets'] - row['liabilities'] - row['equity']:.1f}, "
        f"cash floor={'pass' if row['cash'] >= 2_000.0 else 'FAIL'}"
        for row in results
    )


def evaluate(direct_growth: tuple[float, ...], margin_recovery: tuple[float, ...]) -> dict[str, float | str]:
    """Use fresh immutable tuples for a full, linked model run."""
    results = project(tuple(direct_growth), tuple(margin_recovery))
    equity_value, value_per_share = value_equity(results)
    return {
        "operating_income": results[-1]["operating_income"],
        "fcfe": results[-1]["fcfe"],
        "value_per_share": value_per_share,
        "checks": check_summary(results),
    }


def print_driver(name: str, cases: dict[str, tuple[float, ...]]) -> None:
    print(f"\n{name}")
    print("Input values are FY2027E, FY2028E, FY2029E, FY2030E, FY2031E.")
    base = (evaluate(cases["Base"], CHANNEL_MIX_MARGIN_RECOVERY)
            if name == "Direct revenue growth"
            else evaluate(DIRECT_GROWTH, cases["Base"]))
    all_runs: list[dict[str, float | str]] = []
    for case, path in cases.items():
        # Reset the non-selected driver to its base tuple for every independent run.
        run = evaluate(path, CHANNEL_MIX_MARGIN_RECOVERY) if name == "Direct revenue growth" else evaluate(DIRECT_GROWTH, path)
        all_runs.append(run)
        changes = ("n/a" if case == "Base" else
                   f"OI {run['operating_income'] - base['operating_income']:+.1f}; "
                   f"FCFE {run['fcfe'] - base['fcfe']:+.1f}; "
                   f"value/share {run['value_per_share'] - base['value_per_share']:+.2f}")
        print(
            f"{case:<6} | {', '.join(f'{value:.1%}' for value in path)} | "
            f"FY2031 operating income ${run['operating_income']:,.1f}m | "
            f"FY2031 FCFE ${run['fcfe']:,.1f}m | value/share ${run['value_per_share']:,.2f} | "
            f"change from base: {changes}\n  Checks: {run['checks']}"
        )
    for metric, label, decimals in (
        ("operating_income", "FY2031 operating-income span", 1),
        ("fcfe", "FY2031 FCFE span", 1),
        ("value_per_share", "value-per-share span", 2),
    ):
        values = [float(run[metric]) for run in all_runs]
        print(f"{label}: ${max(values) - min(values):,.{decimals}f}" + ("m" if metric != "value_per_share" else ""))


def main() -> None:
    initial_base = evaluate(DIRECT_GROWTH, CHANNEL_MIX_MARGIN_RECOVERY)
    print("NIKE Lab 11 sensitivity — USD millions except per-share data")
    print("Base input set retained separately; every run uses immutable fresh tuples.")
    print_driver("Direct revenue growth", DIRECT_GROWTH_CASES)
    print_driver("Channel-mix gross-margin recovery", CHANNEL_MIX_MARGIN_RECOVERY_CASES)
    restored_base = evaluate(DIRECT_GROWTH, CHANNEL_MIX_MARGIN_RECOVERY)
    print("\nRestored-base check")
    for metric in ("operating_income", "fcfe", "value_per_share"):
        print(f"{metric}: initial={initial_base[metric]:.6f}; restored={restored_base[metric]:.6f}; "
              f"difference={restored_base[metric] - initial_base[metric]:+.6f}")
    print(f"Checks after restored base: {restored_base['checks']}")


if __name__ == "__main__":
    main()
