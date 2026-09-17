"""Nike P/E comparable-company analysis for the September 10, 2026 valuation date.

All inputs are editable and per share. This is an equity (P/E) comparison: do
not add cash, subtract debt, or otherwise bridge enterprise value to equity.
"""

from decimal import Decimal, InvalidOperation
from statistics import median


# EDITABLE INPUTS ------------------------------------------------------------
TARGET = {
    "symbol": "NKE",
    "name": "Nike",
    "price": "36.62",
    "diluted_eps": "2.10",  # FY2026 GAAP diluted EPS
}

# Include only peers admitted by the written peer policy. See lab08_nike_pe.md.
PEERS = [
    {
        "symbol": "LULU",
        "name": "lululemon athletica",
        "price": "96.88",
        "diluted_eps": "13.26",  # fiscal 2025 GAAP diluted EPS
    },
]


def as_decimal(value):
    """Convert an editable input to Decimal, returning None if it is invalid."""
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


def valid_price_and_eps(company):
    price = as_decimal(company.get("price"))
    eps = as_decimal(company.get("diluted_eps"))
    if price is None or eps is None or price <= 0 or eps <= 0:
        return None
    return price, eps


def clean_peers(target, candidates):
    """Remove the target and repeated ticker symbols, retaining the first peer."""
    target_symbol = str(target.get("symbol", "")).upper()
    seen = set()
    clean = []
    notes = []
    for company in candidates:
        symbol = str(company.get("symbol", "")).upper()
        if symbol == target_symbol:
            notes.append(f"{symbol}: target excluded")
        elif symbol in seen:
            notes.append(f"{symbol}: duplicate excluded")
        else:
            seen.add(symbol)
            clean.append(company)
    return clean, notes


def money(value):
    return f"${value:.2f}"


def main():
    target_values = valid_price_and_eps(TARGET)
    target_eps = as_decimal(TARGET.get("diluted_eps"))
    peers, notes = clean_peers(TARGET, PEERS)

    print("Nike: Comparable-Company P/E Analysis")
    print("Valuation date: September 10, 2026")
    print("P/E = price per share / annual GAAP diluted EPS.")
    if target_values is None:
        print("Target observed P/E: not meaningful (price and EPS must both be positive)")
    else:
        target_price, target_diluted_eps = target_values
        print(f"Target observed P/E: {target_price / target_diluted_eps:.6f}x")

    for note in notes:
        print(f"Peer-screening note: {note}")

    usable = []
    print("\nPeer P/E multiples:")
    for peer in peers:
        values = valid_price_and_eps(peer)
        label = f"{peer['name']} ({peer['symbol']})"
        if values is None:
            print(f"  {label}: not meaningful (price and EPS must both be positive)")
            continue
        price, eps = values
        pe = price / eps
        usable.append((peer, pe))
        print(f"  {label}: {pe:.6f}x")

    if not usable:
        print("\nImplied value: no usable peers.")
        return
    if target_eps is None or target_eps <= 0:
        print("\nImplied value: not meaningful (target diluted EPS must be positive).")
        return

    multiples = [pe for _, pe in usable]
    full_median = Decimal(str(median(multiples)))
    full_estimate = full_median * target_eps
    print(f"\nPeer median P/E: {full_median:.6f}x")

    if len(usable) == 1:
        print("One valid peer: reference estimate, no range.")
        print(f"Nike at peer P/E: {money(full_estimate)}")
    else:
        low = min(multiples) * target_eps
        high = max(multiples) * target_eps
        print("\nNike implied prices:")
        print(f"  Minimum peer P/E: {money(low)}")
        print(f"  Median peer P/E:  {money(full_estimate)}")
        print(f"  Maximum peer P/E: {money(high)}")
        print(f"  Peer-implied range: {money(low)} to {money(high)}")

    print("\nLeave-one-peer-out (relative to the full-peer median estimate):")
    for removed_peer, _ in usable:
        remaining = [pe for peer, pe in usable if peer is not removed_peer]
        if not remaining:
            print(f"  Remove {removed_peer['symbol']}: no estimate (no peers remain)")
            continue
        remaining_median = Decimal(str(median(remaining)))
        remaining_estimate = remaining_median * target_eps
        print(
            f"  Remove {removed_peer['symbol']}: {money(remaining_estimate)} "
            f"({remaining_estimate - full_estimate:+.2f} from full-peer estimate)"
        )


if __name__ == "__main__":
    main()
