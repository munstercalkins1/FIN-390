"""NIKE peer-multiple cross-check, USD millions except share prices.

Run: python nike_peer_multiples.py
Inputs and primary-source locators are documented in PEER_MULTIPLES.md.
"""

from pathlib import Path


VALUATION_DATE = "2026-09-10"

# Same-date share prices; period-end basic shares outstanding for EV calculation.
# EBIT is FY2026 reported EBIT less the documented $986m IEEPA tariff-recovery benefit.
TARGET = {
    "name": "NIKE", "price": 36.62, "shares": 1_483.498703,
    "cash_and_investments": 9_027.0, "debt": 7_942.0,
    "normalized_ebit": 3_850.0 - 986.0,
}
PEER = {
    "name": "lululemon", "price": 96.88, "shares": 110.482671,
    "cash_and_investments": 1_807.202, "debt": 0.0,
    "ebit": 2_210.615,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def enterprise_value(company: dict[str, float | str]) -> float:
    price = float(company["price"])
    shares = float(company["shares"])
    cash = float(company["cash_and_investments"])
    debt = float(company["debt"])
    require(price > 0 and shares > 0, "Price and shares must be positive.")
    return price * shares + debt - cash


def main() -> None:
    target_ev = enterprise_value(TARGET)
    peer_ev = enterprise_value(PEER)
    peer_ebit = float(PEER["ebit"])
    target_ebit = float(TARGET["normalized_ebit"])
    require(peer_ebit > 0 and target_ebit > 0, "EV/EBIT requires positive EBIT.")

    peer_ev_ebit = peer_ev / peer_ebit
    implied_target_ev = peer_ev_ebit * target_ebit
    implied_target_equity = implied_target_ev - float(TARGET["debt"]) + float(TARGET["cash_and_investments"])
    implied_per_share = implied_target_equity / float(TARGET["shares"])
    target_ev_ebit = target_ev / target_ebit

    report = f"""# NIKE Peer Multiples Output

Valuation date: {VALUATION_DATE}. USD millions except per-share figures. Enterprise value = same-date equity value + debt - cash and short-term investments.

| Company | Equity value | Debt | Cash / investments | Enterprise value | EBIT basis | EV / EBIT |
|---|---:|---:|---:|---:|---:|---:|
| NIKE (observed) | ${TARGET['price'] * TARGET['shares']:,.1f} | ${TARGET['debt']:,.1f} | ${TARGET['cash_and_investments']:,.1f} | ${target_ev:,.1f} | ${target_ebit:,.1f} normalized | {target_ev_ebit:.2f}x |
| lululemon (peer) | ${PEER['price'] * PEER['shares']:,.1f} | ${PEER['debt']:,.1f} | ${PEER['cash_and_investments']:,.1f} | ${peer_ev:,.1f} | ${peer_ebit:,.1f} reported | {peer_ev_ebit:.2f}x |

## Qualified EV/EBIT reference

Applying lululemon's {peer_ev_ebit:.2f}x EV/EBIT to NIKE's ${target_ebit:,.1f} normalized EBIT implies:

- Enterprise value: ${implied_target_ev:,.1f}
- Equity value after NIKE cash and debt bridge: ${implied_target_equity:,.1f}
- Per-share reference: **${implied_per_share:.2f}**

This is a one-peer cross-check, not a valuation range or a target price. The multiple is not averaged with the DCF because lululemon's scale, product mix, channel mix, fiscal period, and operating margin differ materially from NIKE's. See `PEER_MULTIPLES.md` for the policy, sources, definitions, and limitations.
"""
    Path("nike_peer_multiples_output.md").write_text(report, encoding="utf-8")
    print(report)
    print("Wrote nike_peer_multiples_output.md")


if __name__ == "__main__":
    main()
