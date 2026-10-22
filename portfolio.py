"""Long-only portfolio search engine for Lab 15.

The Meridian return inputs are estimates, not forecasts.  Run this file with
``python portfolio.py`` to see the original training calculation.
"""

from __future__ import annotations

import csv
import math
from itertools import product
from pathlib import Path


# Meridian training inputs. Values are annual decimal estimates.
MERIDIAN_ASSETS = ["Bills", "10-year", "IG", "Equity"]
MERIDIAN_RETURNS = {"Bills": 0.030, "10-year": 0.043, "IG": 0.050, "Equity": 0.080}
MERIDIAN_VOLATILITIES = {"Bills": 0.200, "10-year": 0.080, "IG": 0.070, "Equity": 0.160}
MERIDIAN_CORRELATIONS = {
    "Bills": {"Bills": 1.00, "10-year": 0.05, "IG": 0.05, "Equity": 0.00},
    "10-year": {"Bills": 0.05, "10-year": 1.00, "IG": 0.249, "Equity": -0.126},
    "IG": {"Bills": 0.05, "10-year": 0.249, "IG": 1.00, "Equity": 0.266},
    "Equity": {"Bills": 0.00, "10-year": -0.126, "IG": 0.266, "Equity": 1.00},
}
MERIDIAN_RESERVE_ELIGIBLE = {"Bills", "10-year"}
MERIDIAN_OBJECTIVE = 0.065
MERIDIAN_RESERVE_MINIMUM = 0.03


def portfolio_metrics(weights: dict[str, float], expected_returns: dict[str, float],
                      volatilities: dict[str, float], correlations: dict[str, dict[str, float]]) -> tuple[float, float]:
    """Return annual expected return and volatility for a set of weights."""
    assets = list(expected_returns)
    expected_return = sum(weights.get(asset, 0.0) * expected_returns[asset] for asset in assets)
    variance = sum(
        weights.get(left, 0.0) * weights.get(right, 0.0)
        * volatilities[left] * volatilities[right] * correlations[left][right]
        for left in assets for right in assets
    )
    return expected_return, math.sqrt(max(0.0, variance))


def search_lowest_risk_mix(expected_returns: dict[str, float], volatilities: dict[str, float],
                           correlations: dict[str, dict[str, float]], objective: float,
                           reserve_eligible: set[str] | list[str], reserve_minimum: float,
                           step: float = 0.05) -> dict[str, object] | None:
    """Try every long-only ``step`` mix and return the feasible least-risk mix.

    A result is ``None`` when no mixture reaches both the return objective and
    reserve floor.  Inputs and outputs use decimals (0.065 means 6.5%).
    """
    assets = list(expected_returns)
    if not assets or set(assets) != set(volatilities):
        raise ValueError("returns and volatilities must contain the same assets")
    units = round(1 / step)
    if not math.isclose(units * step, 1.0, abs_tol=1e-10):
        raise ValueError("step must divide 100% exactly")
    reserve_eligible = set(reserve_eligible)
    best: dict[str, object] | None = None
    # The final asset receives the remaining units, so all tested weights sum to 100%.
    for first_units in product(range(units + 1), repeat=len(assets) - 1):
        final_units = units - sum(first_units)
        if final_units < 0:
            continue
        weights = {asset: count * step for asset, count in zip(assets, (*first_units, final_units))}
        expected_return, volatility = portfolio_metrics(weights, expected_returns, volatilities, correlations)
        reserve_weight = sum(weights[asset] for asset in assets if asset in reserve_eligible)
        if expected_return + 1e-12 < objective or reserve_weight + 1e-12 < reserve_minimum:
            continue
        candidate = {"weights": weights, "return": expected_return, "volatility": volatility,
                     "reserve_weight": reserve_weight}
        if best is None or volatility < best["volatility"] - 1e-12:
            best = candidate
    return best


def estimate_from_prices(csv_source: str | Path | object, last_36_months: bool = False) -> tuple[dict[str, float], dict[str, float], dict[str, dict[str, float]]]:
    """Estimate annual return, volatility, and correlations from monthly prices.

    The CSV must have a date as its first column and one price column per ticker,
    oldest month first. Returns are arithmetic monthly means × 12 and sample
    standard deviations × sqrt(12); these are historical estimates, not forecasts.
    """
    close_after = False
    if isinstance(csv_source, (str, Path)):
        handle = open(csv_source, newline="", encoding="utf-8-sig")
        close_after = True
    else:
        handle = csv_source
    try:
        rows = list(csv.reader(handle))
    finally:
        if close_after:
            handle.close()
    if len(rows) < 3 or len(rows[0]) < 2:
        raise ValueError("CSV needs a date column, one or more tickers, and at least three price rows")
    tickers = [item.strip() for item in rows[0][1:]]
    if not all(tickers) or len(set(tickers)) != len(tickers):
        raise ValueError("ticker headers must be present and unique")
    prices = []
    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(tickers) + 1:
            raise ValueError(f"row {row_number} does not match the header")
        try:
            prices.append([float(value.replace(",", "")) for value in row[1:]])
        except ValueError as error:
            raise ValueError(f"row {row_number} has a non-numeric price") from error
    if any(value <= 0 for row in prices for value in row):
        raise ValueError("prices must be positive")
    returns = [[prices[row][col] / prices[row - 1][col] - 1 for col in range(len(tickers))]
               for row in range(1, len(prices))]
    if last_36_months:
        returns = returns[-36:]
    if len(returns) < 2:
        raise ValueError("need at least three prices (two monthly returns)")
    means = [sum(row[col] for row in returns) / len(returns) for col in range(len(tickers))]
    stdevs = [math.sqrt(sum((row[col] - means[col]) ** 2 for row in returns) / (len(returns) - 1))
              for col in range(len(tickers))]
    annual_returns = {ticker: means[index] * 12 for index, ticker in enumerate(tickers)}
    annual_volatilities = {ticker: stdevs[index] * math.sqrt(12) for index, ticker in enumerate(tickers)}
    correlations: dict[str, dict[str, float]] = {ticker: {} for ticker in tickers}
    for left, left_ticker in enumerate(tickers):
        for right, right_ticker in enumerate(tickers):
            if left == right:
                value = 1.0
            elif stdevs[left] == 0 or stdevs[right] == 0:
                value = 0.0
            else:
                covariance = sum((row[left] - means[left]) * (row[right] - means[right]) for row in returns) / (len(returns) - 1)
                value = covariance / (stdevs[left] * stdevs[right])
            correlations[left_ticker][right_ticker] = value
    return annual_returns, annual_volatilities, correlations


def main() -> None:
    answer = search_lowest_risk_mix(MERIDIAN_RETURNS, MERIDIAN_VOLATILITIES, MERIDIAN_CORRELATIONS,
                                    MERIDIAN_OBJECTIVE, MERIDIAN_RESERVE_ELIGIBLE, MERIDIAN_RESERVE_MINIMUM)
    print("Meridian lowest-risk mix (5-point steps)")
    if answer is None:
        print("No mix meets the objective.")
        return
    print(" / ".join(f"{asset} {answer['weights'][asset]:.0%}" for asset in MERIDIAN_ASSETS))
    print(f"Return: {answer['return']:.2%}")
    print(f"Volatility: {answer['volatility']:.2%}")
    print(f"Reserve-eligible weight: {answer['reserve_weight']:.2%}")


if __name__ == "__main__":
    main()
