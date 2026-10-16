# Project 1 Edition B - NIKE, Inc. (NYSE: NKE)

## Committee decision

**Decision user: ** Buy-side investment committee.  
**Decision horizon: ** Five-year operating forecast, with terminal value only as a continuing-value convention.  
**Valuation date:** September 10, 2026. **Currency: ** USD.  
**Security: ** NIKE Class B common stock. **Share basis: ** FY2026 diluted weighted-average shares of 1,481.0m for the DCF; period-end common shares outstanding only for the EV multiple. The difference is disclosed rather than silently blended.

**Action: Watch / defer. ** The FCFF DCF produces a causal downside-to-upside range of **$28.52-$62.20 per share**, with a base case of **$44.68**, against a same-date market reference of **$36.62*. The base case requires Direct stabilization, a gradual margin recovery that does not rely on the IEEPA tariff benefit, constructive wholesale sales, and sound cash conversion. Those requirements are not sufficiently demonstrated to be initiated now.

Move toward initiation only if subsequent disclosures confirm stabilization in Direct and digital sales, recurring growth margin improvement, and controlled inventory/receivables. Move toward do-not-initiate if Direct weakness, Greater China/Converse deterioration, promotional pressure, or poor cash conversion persists, or if the market price exceeds the high case without new evidence.

## Evidence and method map

| Required element | Evidence |
|---|---|
| Source distinctions and base-year normalization | `SOURCE_MAP.md` |
| Load-bearing assumptions and challenges | `ASSUMPTION_REGISTER.md` |
| Five-year linked three-statement FCFF engine | `nike_fcff_application.py` |
| Visible output, DCF range, sensitivity, terminal-value share, reverse DCF | `nike_fcff_output.md` |
| Equity-value multiple | `lab08_nike_pe.md`, `nike_pe_comparison.py` |
| Enterprise-value multiple | `PEER_MULTIPLES.md`, `nike_peer_multiples.py`, `nike_peer_multiples_output.md` |
| Validation, AI-use disposition, high-risk failure test, cold-run record | `VALIDATION_RECORD.md` |
| Full committee rationale and method disagreement | `COMMITTEE_MEMO.md` |

## Method disagreement

The DCF is the primary method because it models NIKE's specific operating recovery explicitly. The one-peer P/E and EV/EBIT references are intentionally not averaged into it: lululemon has a different scale, product mix, channel exposure, fiscal calendar, and margin profile. Their lower outputs are a warning that the recovery embedded in the DCF needs evidence, not a mathematical instruction to average unlike methods.

