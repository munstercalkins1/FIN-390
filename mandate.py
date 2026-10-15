"""Lab 13 — Meridian Foundation Reserve mandate checker.

Run with: python mandate.py
All inputs are collected in the two editable tables below.
"""

# Editable inputs
HOLDINGS = {
    "Cash": {"issuer": "none", "days": 0, "reserve_eligible": True},
    "Treasury bills": {"issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True},
    "Treasury 10-year note": {"issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True},
    "Global equity index fund": {"issuer": "diversified fund", "days": 2, "reserve_eligible": False},
    "Investment-grade bond fund": {"issuer": "diversified fund", "days": 3, "reserve_eligible": False},
    "Private real estate fund": {"issuer": "diversified fund", "days": 90, "reserve_eligible": False},
    "Acme Corp bonds": {"issuer": "Acme Corp", "days": 4, "reserve_eligible": False},
    "Acme Corp stock": {"issuer": "Acme Corp", "days": 1, "reserve_eligible": False},
}

CANDIDATES = {
    "A": {"Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
          "Global equity index fund": 60, "Investment-grade bond fund": 26,
          "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0},
    "B": {"Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
          "Global equity index fund": 55, "Investment-grade bond fund": 20,
          "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4},
    "C": {"Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
          "Global equity index fund": 70, "Investment-grade bond fund": 20,
          "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8},
    # Attack portfolio: it passes the coded rules but may not pursue the return objective.
    "D": {"Cash": 10, "Treasury bills": 90, "Treasury 10-year note": 0,
          "Global equity index fund": 0, "Investment-grade bond fund": 0,
          "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0},
}

RESERVE_SIZE = 100  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5  # business days
MINIMUM_LIQUID_SHARE = 90  # percent
ISSUER_LIMIT = 8  # percent
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def verdict(value, passes):
    """Format every tested quantity consistently."""
    return f"{value:.1f} {'pass' if passes else 'FAIL'}"


def check_candidate(name, weights, reserve_minimum):
    """Measure only rules whose terms can be checked from the supplied inputs."""
    failures = 0

    total = sum(weights.values())
    passes = total == 100
    failures += not passes
    print(f"Weights sum to 100: {verdict(total, passes)}")

    lowest = min(weights.values())
    passes = lowest >= 0
    failures += not passes
    print(f"Long-only (lowest weight): {verdict(lowest, passes)}")

    reserve_weight = sum(weights[holding] for holding, details in HOLDINGS.items()
                         if details["reserve_eligible"])
    passes = reserve_weight >= reserve_minimum
    failures += not passes
    print(f"Reserve >= {reserve_minimum:.1f}%: {verdict(reserve_weight, passes)}")

    liquid_weight = sum(weights[holding] for holding, details in HOLDINGS.items()
                        if details["days"] <= LIQUIDITY_WINDOW)
    passes = liquid_weight >= MINIMUM_LIQUID_SHARE
    failures += not passes
    print(f"Redeemable in {LIQUIDITY_WINDOW} days >= {MINIMUM_LIQUID_SHARE:.0f}%: "
          f"{verdict(liquid_weight, passes)}")

    company_totals = {}
    for holding, details in HOLDINGS.items():
        issuer = details["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            company_totals[issuer] = company_totals.get(issuer, 0) + weights[holding]
    largest_company = max(company_totals.values(), default=0)
    passes = largest_company <= ISSUER_LIMIT
    failures += not passes
    print(f"Largest single company <= {ISSUER_LIMIT:.0f}%: {verdict(largest_company, passes)}")

    print("Calendar-year loss: requires CIO clarification")
    if failures:
        print(f"{name} fails {failures} rule(s)")
    else:
        print(f"{name} passes every checkable rule")


def main():
    reserve_minimum = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    print(f"Reserve minimum: {reserve_minimum:.1f}% of the portfolio")
    for name, weights in CANDIDATES.items():
        print(f"\nCandidate {name}")
        check_candidate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()
