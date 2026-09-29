# Lab 11 — NIKE sensitivity analysis

All dollar values are USD millions except value per share. Forecast years are FY2027E–FY2031E. The cash-flow measure is **FCFE** (free cash flow to equity), consistent with the existing equity valuation.

## Locked changed-input record

Locked at **2026-09-29 13:50 EDT**, before the sensitivity runs.

| Driver | Base → lower / higher | Affected years and units | Prediction and reason |
|---|---|---|---|
| Direct revenue growth | 0.0%, 1.5%, 3.0%, 3.5%, 2.5% → each year −2.0 percentage points / +2.0 percentage points | FY2027E–FY2031E; percentage points of Direct-channel revenue growth | Higher Direct growth should increase consolidated revenue, then gross profit and operating income. I expected a positive but moderated FCFE/value effect because higher revenue also requires working capital and capex. The range brackets a slower recovery after Direct revenue fell 6% in FY2026, versus a modest improvement if traffic and digital demand recover. |
| Channel-mix gross-margin recovery | 60, 110, 160, 210, 210 bps → each year −100 bps / +100 bps | FY2027E–FY2031E; basis points added to FY2026’s 42.9% gross margin | Higher recovery should increase gross profit and operating income directly, then FCFE and value. I expected this driver to be important because the existing model’s S&A is calculated from gross profit. The range brackets promotion/discount pressure continuing versus a return toward NIKE’s FY2024 44.6% gross margin. |

The lower and higher cases change one independent input only. The non-selected driver is reset to its base path before every run; all statement links recalculate.

## Actual sensitivity results

### Direct revenue growth

| Case | Direct growth input: FY27, FY28, FY29, FY30, FY31 | FY2031 operating income | FY2031 FCFE | Value/share | Change from base: operating income | Change from base: FCFE | Change from base: value/share | Accounting check |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Lower | −2.0%, −0.5%, 1.0%, 1.5%, 0.5% | $5,592.7 | $4,603.4 | $42.79 | −$211.2 | −$65.6 | −$0.46 | Pass: all balance-sheet gaps round to $0.0; cash stays above $2,000m floor |
| Base | 0.0%, 1.5%, 3.0%, 3.5%, 2.5% | $5,803.9 | $4,669.0 | $43.25 | $0.0 | $0.0 | $0.00 | Pass |
| Higher | 2.0%, 3.5%, 5.0%, 5.5%, 4.5% | $6,021.5 | $4,734.2 | $43.71 | +$217.5 | +$65.2 | +$0.45 | Pass |
| **Span (max − min)** | — | **$428.7** | **$130.8** | **$0.91** | — | — | — | — |

Trace for the higher case: a higher Direct growth path raises the revenue line; gross profit rises at the unchanged gross-margin path; S&A rises because it is linked to gross profit; operating income rises. Inventory, receivables, payables, other assets, other liabilities, and capex then recalculate from revenue/COGS, reducing the FCFE pass-through relative to operating income.

### Channel-mix gross-margin recovery

| Case | Margin-recovery input: FY27, FY28, FY29, FY30, FY31 | FY2031 operating income | FY2031 FCFE | Value/share | Change from base: operating income | Change from base: FCFE | Change from base: value/share | Accounting check |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Lower | −40, 10, 60, 110, 110 bps | $5,674.9 | $4,563.8 | $42.24 | −$129.0 | −$105.2 | −$1.02 | Pass: all balance-sheet gaps round to $0.0; cash stays above $2,000m floor |
| Base | 60, 110, 160, 210, 210 bps | $5,803.9 | $4,669.0 | $43.25 | $0.0 | $0.0 | $0.00 | Pass |
| Higher | 160, 210, 260, 310, 310 bps | $5,932.9 | $4,774.1 | $44.27 | +$129.0 | +$105.2 | +$1.02 | Pass |
| **Span (max − min)** | — | **$258.0** | **$210.3** | **$2.03** | — | — | — | — |

Trace for the higher case: a higher recovery path raises gross margin at unchanged revenue. This raises gross profit; linked S&A rises as a percentage of gross profit, but less than gross profit, so operating income rises. The gain flows through net income and FCFE. Since the model holds inventory days and payables-to-COGS constant, lower COGS also changes working-capital balances.

## Restored-base and calculation checks

The independent base paths were retained separately and rerun after all six sensitivity runs. Initial base and restored base agree within a $0.000001m / $0.000001 per-share rounding tolerance:

| Output | Initial base | Restored base | Difference |
|---|---:|---:|---:|
| FY2031 operating income | $5,803.924053m | $5,803.924053m | $0.000000m |
| FY2031 FCFE | $4,668.970439m | $4,668.970439m | $0.000000m |
| Value per share | $43.253132 | $43.253132 | $0.000000 |

For every usable run, `assets − liabilities − equity` was zero before rounding (less than $0.000001m in absolute value) in each forecast year, and cash was above the $2,000m floor. The FCFE/value changes in the tables are each result minus the corresponding base result; for example, the higher-margin FCFE change is $4,774.1m − $4,669.0m = +$105.2m.

## Finding and interpretation

Over these ranges, **Direct revenue growth is the larger driver of FY2031 operating income** ($428.7m span versus $258.0m). **Channel-mix gross-margin recovery is the larger driver of FY2031 FCFE and value per share** ($210.3m versus $130.8m FCFE span; $2.03 versus $0.91 per-share span). The valuation is available because the FCFE stream is positive and the existing FCFE terminal-value method remains valid in every case.

This is a ranking **over these ranges**, not proof that margin is inherently more important than revenue. The selected ±100 bps margin range and the five-year compounding/terminal-value link influence the comparison. A wider Direct-growth range could change the ranking.

My locked prediction was directionally correct. The notable result is that Direct growth produces the greater final-year operating-income span, but margin produces the greater FCFE and value span. That difference occurs because the margin change affects cash generation throughout the forecast without the additional revenue-linked investment requirements, and value incorporates the terminal FCFE.

The sensitivity does not assign probabilities: each row is a conditional result for a deliberately chosen input, not an estimate of the likelihood of that input or of the output. It changes my research priority toward evidence on promotion/discount intensity, product cost, and channel mix, while I still need to monitor Direct traffic and digital demand. My valuation conclusion remains conditional: the $43.25 base value is more exposed to the assumed margin recovery than to the tested Direct-growth path.

## Partner exchange notes — complete with actual partner interaction

Do not submit the prompts below as completed evidence. Replace brackets after the exchanges.

| Exchange | My note |
|---|---|
| 1 — question received and my response | **Partner’s question:** “What was the main driver?” **My response:** “Revenue.” I explained that higher revenue increases the forecast’s sales and operating profit, which can increase FCFE and equity value. |
| 1 — check performed on partner | My partner challenged my initial revenue conclusion by pointing out that gross profit can change the outcome substantially. I recorded this as a limitation: the driver ranking depends on the stated ranges, and margin recovery is the larger driver of my FCFE and value results. |
| 2 — check performed on partner’s result | I checked the conceptual link in my partner’s Microsoft analysis: a revenue assumption should flow through operating profit and cash flow before it changes equity value. I did not record a separate numerical recomputation during this exchange. |
| 2 — question/correction received | My partner’s correction was that gross profit can materially change the result, even when revenue is the proposed main driver. I revised my conclusion to distinguish final-year operating income (Direct revenue growth has the larger span) from FCFE and value per share (margin recovery has the larger span). |
| 3 — question received and my answer | **My question to partner:** “How did revenue growth actually improve equity value?” **Partner’s answer:** “Investors demand more for developments related to AI.” I noted that this explains market demand for the company but not the pro-forma mechanism; the model link still needs to be revenue growth → profit/FCFE → discounted equity value. |
| 3 — my summary of partner’s conclusion | For Microsoft, my partner identified revenue from recent AI-related innovations as the main driver. Its limitation is that the conclusion depends on the selected revenue range and on how the model translates revenue into margins, investment needs, cash flow, and value. |

## Learn on your own

One-at-a-time sensitivity changes one independent assumption to a specified alternative while holding all other independent assumptions at their base values, then lets linked statements recalculate. The chosen input range affects the ranking because the reported span measures both the model’s responsiveness and the size of the assumed change. A sensitivity table is not a forecast probability because it supplies scenarios without likelihoods, correlations, or a distribution of future outcomes.

## Files and run command

- `nike_lab10_proforma.py` — original linked pro-forma, extended so `project()` accepts fresh driver paths.
- `nike_lab11_sensitivity.py` — sensitivity runner; after Python is available on PATH, run `python nike_lab11_sensitivity.py`.
- `lab11_nike_sensitivity.md` — visible result and write-up.

Terminal note: Python 3.13.15 was installed for this Windows user and successfully ran `nike_lab11_sensitivity.py` on 2026-09-29. The output matched the visible results above, all accounting checks passed, and the restored-base differences were zero. The current terminal session may need to be closed and reopened before the new PATH entry makes `python nike_lab11_sensitivity.py` available; the interpreter path used for verification was `%LocalAppData%\Programs\Python\Python313\python.exe`.
