# Validation and AI-Use Record

## Tests implemented in `nike_fcff_application.py`

| Required check | Implementation / expected evidence |
|---|---|
| Synthetic known-answer reconciliation | Five annual FCFF values of $100, WACC 10%, terminal growth 0%; code recomputes the analytical enterprise value and requires equality within $0.0001m. |
| Independent source/definition check | FY2026 revenue and inventory are independently traced to the 10-K pp. 55 and 57 in `SOURCE_MAP.md`; student must initial after opening the filing. |
| Base-year reconciliation | FY2026 assets equal liabilities plus equity using balance-sheet facts from the filing. |
| Forecast articulation | Every forecast year requires balance-sheet gap under $0.01m and cash-flow change to equal the change in balance-sheet cash. |
| DCF boundary / monotonicity | Value must fall as WACC rises from 8% to 10%, and rise as terminal growth rises from 2% to 3%. |
| EV-to-equity bridge | Code recomputes equity value as EV + cash + investments − debt. |
| High-risk failure test | Deliberately change one projected cash amount without changing the cash-flow statement; expected result is a fail-loud balance-sheet error. Actual result on Oct. 14, 2026: `PASS — expected fail-loud articulation error: FY2027 cash-flow-to-cash tie failed.` |
| Cold run | In a fresh folder/environment, copy only the application, run it, and retain the command plus resulting output timestamp. |
| Peer/multiple consistency | `lab08_nike_pe.md` uses price / annual GAAP diluted EPS consistently and says the one-peer result is a reference, not a range. |

## Locked Changed-Input Record — human-authored section

This prediction must be written by the student with AI off, committed/timestamped before execution, then frozen. Do not backdate it.

| Field | Record |
|---|---|
| Precommit timestamp / commit | 2026-10-15 19:00:11 -04:00; local save completed before execution; Git commit unavailable in this terminal. |
| Input and units | [e.g., FY2027E Direct growth: 0.0% to -4.0%, percentage points] |
| Old / new value | [enter] |
| Human prediction of output direction | I think that Nike value goes down in my model because revenue growth stays weaker, like 0 percent in FY 2027 to -4 percent. |
| Reason | Nike has a lot of fixed costs (marketing, stores, warehoues) so they dont get as much as operating leverage and EBIT Come back more slowly. Less ebit means less fcff, since there is less money left. The main risk is that I am being to conservative and the stock could be overvalued right now. |
| Actual direction / result | Decreased as predicted: base intrinsic value fell from $44.68 per share to $44.17 per share (down $0.51) when FY2027E Direct growth changed from 0.0% to -4.0%. All five model validation checks passed. |
| Decision effect | No change to the conditional watch/defer action: the lower value remains above the $36.62 same-date market reference, but the result reinforces that evidence on Direct stabilization matters before initiating. |
| Failure diagnosis or no-change reason | No validation failure and no unexpected direction. The lower Direct-revenue path reduced forecast revenue, EBIT, FCFF, and DCF value as predicted. |

## AI output disposition

| AI-assisted item | Independent evidence checked | Disposition | Student correction / qualification |
|---|---|---|---|
| Model scaffold and narrative organization | FY2026 10-K pp. 35, 55, 57–58; source map above | Qualified | Forecasts are student judgments; the student must verify every filing locator and not present AI text as a primary source. |

## Cold-run log

| Date / environment | Command | Result | Output retained |
|---|---|---|---|
| Oct. 14, 2026; Python 3.13.15; newly created temporary working directory containing only the application | `python nike_fcff_application.py` | Pass; visible output created, including all five validation passes | `nike_fcff_output.md` |
