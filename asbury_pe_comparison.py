"""Asbury Automotive peer P/E comparison using the Lab 07 frozen case inputs.

All inputs are per share and editable.  This is an equity-value comparison:
do not add cash, subtract debt, or otherwise bridge enterprise value to equity.
"""

from decimal import Decimal, InvalidOperation
from statistics import median


# EDITABLE INPUTS ------------------------------------------------------------
TARGET = {
    "symbol": "ABG",
    "name": "Asbury Automotive",
    "price": "243.03",
    "diluted_eps": "21.50",
}

PEERS = [
    {
        "symbol": "AN",
        "name": "AutoNation",
        "price": "169.84",
        "diluted_eps": "16.92",
    },
    {
        "symbol": "GPI",
        "name": "Group 1 Automotive",
        "price": "421.48",
        "diluted_eps": "36.81",
    },
]


def as_decimal(value):
    """Convert an editable input to Decimal; return None for blank/invalid input."""
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


def valid_price_and_eps(company):
    """Return converted price and EPS when both are positive, otherwise None."""
    price = as_decimal(company.get("price"))
    eps = as_decimal(company.get("diluted_eps"))
    if price is None or eps is None or price <= 0 or eps <= 0:
        return None
    return price, eps


def clean_peers(target, candidates):
    """Exclude the target and repeated ticker symbols, retaining first occurrence."""
    target_symbol = str(target.get("symbol", "")).upper()
    seen_symbols = set()
    accepted = []
    excluded = []
    for company in candidates:
        symbol = str(company.get("symbol", "")).upper()
        if symbol == target_symbol:
            excluded.append(f"{symbol}: target excluded")
        elif symbol in seen_symbols:
            excluded.append(f"{symbol}: duplicate excluded")
        else:
            seen_symbols.add(symbol)
            accepted.append(company)
    return accepted, excluded


def implied_price(pe_multiple, target_eps):
    return pe_multiple * target_eps


def money(value):
    return f"${value:.2f}"


def main():
    target_price_and_eps = valid_price_and_eps(TARGET)
    target_eps = as_decimal(TARGET.get("diluted_eps"))
    peers, exclusions = clean_peers(TARGET, PEERS)

    print("Asbury Case: Comparable-Company P/E Analysis")
    print("Inputs use Dec. 31, 2024 closing prices and FY2024 GAAP diluted EPS.")
    print("P/E = price per share / diluted EPS.")

    if target_price_and_eps is None:
        print("Target observed P/E: not meaningful (price and diluted EPS must both be positive)")
    else:
        target_price, target_diluted_eps = target_price_and_eps
        print(f"Target observed P/E: {target_price / target_diluted_eps:.6f}x")

    if exclusions:
        print("\nPeer-screening notes:")
        for note in exclusions:
            print(f"  {note}")

    usable = []
    print("\nPeer P/E multiples:")
    for peer in peers:
        values = valid_price_and_eps(peer)
        label = f"{peer['name']} ({peer['symbol']})"
        if values is None:
            print(f"  {label}: not meaningful (price and diluted EPS must both be positive)")
            continue
        price, eps = values
        pe_multiple = price / eps
        usable.append((peer, pe_multiple))
        print(f"  {label}: {pe_multiple:.6f}x")

    if not usable:
        print("\nImplied value: no usable peers.")
        return
    if target_eps is None or target_eps <= 0:
        print("\nImplied value: not meaningful (target diluted EPS must be positive).")
        return

    multiples = [pe_multiple for _, pe_multiple in usable]
    full_median = Decimal(str(median(multiples)))
    print(f"\nPeer median P/E: {full_median:.6f}x")

    if len(usable) == 1:
        reference = implied_price(full_median, target_eps)
        print("One valid peer: reference estimate, no range.")
        print(f"Target at peer P/E: {money(reference)}")
        print("\nLeave-one-peer-out (relative to the full-peer median estimate):")
        print(f"  Remove {usable[0][0]['symbol']}: no estimate (no peers remain)")
        return

    low_multiple = min(multiples)
    high_multiple = max(multiples)
    print("\nTarget implied prices (using target diluted EPS):")
    print(f"  Minimum peer P/E: {money(implied_price(low_multiple, target_eps))}")
    print(f"  Median peer P/E:  {money(implied_price(full_median, target_eps))}")
    print(f"  Maximum peer P/E: {money(implied_price(high_multiple, target_eps))}")
    print(
        f"  Peer-implied range: {money(implied_price(low_multiple, target_eps))}"
        f" to {money(implied_price(high_multiple, target_eps))}"
    )

    full_estimate = implied_price(full_median, target_eps)
    print("\nLeave-one-peer-out (relative to the full-peer median estimate):")
    for removed_peer, _ in usable:
        remaining = [multiple for peer, multiple in usable if peer is not removed_peer]
        if not remaining:
            print(f"  Remove {removed_peer['symbol']}: no estimate (no peers remain)")
            continue
        remaining_median = Decimal(str(median(remaining)))
        remaining_estimate = implied_price(remaining_median, target_eps)
        change = remaining_estimate - full_estimate
        range_note = "; reference estimate, no range" if len(remaining) == 1 else ""
        print(
            f"  Remove {removed_peer['symbol']}: {money(remaining_estimate)} "
            f"({change:+.2f} from full-peer estimate){range_note}"
        )


if __name__ == "__main__":
    main()
