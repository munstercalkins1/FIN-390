# Peer Multiples - NIKE, Inc.

## Policy and definitions

This is a cross-check, not a substitute for the five-year FCFF DCF. The peer policy from `lab08_nike_pe.md` admits a listed branded athletic-products operator only when its business model is comparable enough to inform a qualified reference and its audited annual figures are public by the September 10, 2026 valuation date. Lululemon is the only admitted peer; Under Armour remains excluded from the P/E reference because its annual GAAP EPS was negative.

Two definitions are kept separate:

- **Equity-value multiple:** price / annual GAAP diluted EPS (P/E) in `lab08_nike_pe.md`.
- **Enterprise-value multiple:** enterprise value / EBIT (EV/EBIT), where enterprise value = same-date price x period-end basic shares outstanding + total debt - cash and short-term investments. No lease liabilities or non-controlling interests are included for either company; this simplification is applied consistently and disclosed.

For NIKE, EBIT is normalized by excluding the FY2026 $986m IEEPA tariff-recovery benefit in cost of sales. This keeps a temporary recovery from being treated as recurring operating profit. The treatment is not applied to lululemon because no equivalent one-time item was identified for this cross-check.

## Inputs and authoritative sources

| Input | NIKE | lululemon | Source / definition |
|---|---:|---:|---|
| Same-date close | $36.62 | $96.88 | September 10, 2026 regular-session closes; see historical-price links in `lab08_nike_pe.md`. |
| Shares outstanding (m) | 1,483.499 | 110.483 | NIKE FY2026 10-K cover, July 8, 2026; lululemon FY2025 10-K cover, March 11, 2026. Both use actual common shares outstanding, not weighted-average EPS shares. |
| Cash / short-term investments (m) | $9,027.0 | $1,807.202 | [NIKE FY2026 10-K, pp. 57 and 68](https://www.sec.gov/Archives/edgar/data/320187/000032018726000088/nke-20260531.htm); [lululemon FY2025 10-K, liquidity](https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm). |
| Total debt (m) | $7,942.0 | $0.0 | NIKE FY2026 10-K Note 6 (total corporate term debt); lululemon's filing identifies a revolver capacity but no drawn borrowings. |
| EBIT (m) | $2,864.0 normalized | $2,210.615 reported | NIKE FY2026 reported EBIT $3,850.0 less $986.0 IEEPA tariff-recovery benefit; lululemon FY2025 consolidated income from operations. |

Run `python nike_peer_multiples.py` to regenerate [nike_peer_multiples_output.md](nike_peer_multiples_output.md). The calculation checks for positive price, shares, and EBIT. The visible output calculates the observed multiples and the peer-implied NIKE per-share reference from the editable inputs.

## Interpretation

The EV/EBIT result is deliberately a **qualified one-peer reference**. Lululemon is smaller, much more direct-to-consumer and apparel-led, has a different fiscal year-end, and has a different margin profile. Its low same-date EV/EBIT therefore cannot override the DCF or be mechanically averaged with it. The disagreement is informative: the DCF assigns value to NIKE's forecast recovery in Direct, wholesale, and margins, while the peer reference reflects a differently structured public market operator at the valuation date.
