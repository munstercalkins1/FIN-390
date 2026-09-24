# Lab 10 — NIKE, Inc. (NYSE: NKE) Pro-Forma

## Question and company difference

What are five years of NIKE's statements worth, built from assumptions I can defend?

NIKE is different because its brand demand is sold through both wholesale partners and its own Direct channels; the mix matters because Direct traffic, digital demand, and discounting affect revenue and gross margin differently from wholesale. The model names this line **Direct/wholesale channel normalization**. It uses FY2026 wholesale, Direct, and other-revenue weights to calculate consolidated revenue growth from separate channel-growth paths; it then adds only 60 bps of margin recovery in FY2027E, building to 210 bps by FY2030E. These are `WHOLESALE_GROWTH`, `DIRECT_GROWTH`, and `CHANNEL_MIX_MARGIN_RECOVERY` inputs in `nike_lab10_proforma.py`.

All figures are USD millions except per-share data. Fiscal years end May 31.

## History grid and sources

| Item | FY2024 | FY2025 | FY2026 | Filing/source |
|---|---:|---:|---:|---|
| Revenue | 51,362 | 46,309 | 46,398 | FY2026 10-K, Consolidated Statements of Income, p. 55 |
| Gross profit | 22,887 | 19,790 | 19,911 | FY2026 10-K, p. 55 |
| Selling & administrative expense | 16,576 | 16,088 | 16,114 | FY2026 10-K, p. 55 |
| Net income | 5,700 | 3,219 | 3,108 | FY2026 10-K, p. 55 |
| Inventory | 7,519 | 7,489 | 7,501 | FY2024 10-K, p. 59 (FY2024); FY2026 10-K, p. 57 (FY2025–26) |
| PP&E, net | 5,000 | 4,828 | 4,796 | FY2024 10-K, p. 59 (FY2024); FY2026 10-K, p. 57 (FY2025–26) |
| Shareholders’ equity | 14,430 | 13,213 | 14,865 | FY2024 10-K, p. 59 (FY2024); FY2026 10-K, p. 57 (FY2025–26) |

### Your two hand checks

Open the FY2026 10-K and verify these before submitting, then initial or replace the brackets:

| Item checked | Filing location | Result |
|---|---|---|
| FY2026 revenue: $46,398m | FY2026 10-K, p. 55, Consolidated Statements of Income | [initial after checking] |
| FY2026 inventory: $7,501m | FY2026 10-K, p. 57, Consolidated Balance Sheets | [initial after checking] |

FY2024 balance-sheet values come from the FY2024 filing because the FY2026 balance sheet presents only FY2026 and FY2025.

## History-derived ratios

| Ratio / growth measure | FY2024 | FY2025 | FY2026 | Source / calculation |
|---|---:|---:|---:|---|
| Gross margin | 44.6% | 42.7% | 42.9% | Gross profit ÷ revenue; FY2026 10-K pp. 32, 55 |
| S&A ÷ gross profit | 72.4% | 81.3% | 80.9% | S&A ÷ gross profit; FY2026 10-K p. 55 |
| Inventory days | 96.4 | 103.1 | 103.4 | Inventory ÷ cost of sales × 365; 10-K pp. 55, 57 |
| Depreciation & amortization ÷ PP&E | 15.9% | 16.1% | 15.6% | Cash-flow D&A ÷ year-end PP&E; FY2026 10-K pp. 57–58 |
| Capital spending | 812 | 430 | 684 | Filing cash-flow line “Additions to property, plant and equipment,” FY2026 10-K p. 58 |
| Provider capex cross-check (not model source of record) | 812 | 430 | 684 | StockAnalysis cash-flow statement (S&P Global Market Intelligence data), matched to the 10-K capex line; values shown as outflows, so the provider displays them as negative. |
| Effective tax rate | 14.9% | 17.1% | 20.3% | FY2026 10-K p. 35 |
| Reported revenue growth | 0.3% | -9.8% | 0.2% | FY2026 10-K p. 55; calculated from reported revenue |
| Currency-neutral NIKE Brand growth | n/a | -9% | 1% | FY2026 10-K p. 32 |
| Comparable store sales | n/a | not located | -4% | FY2026 10-K p. 33; established NIKE-owned stores only |

NIKE discloses comparable store sales, not company-wide organic growth. It defines the metric as NIKE-owned in-line and factory stores open at least one year, with limited square-footage change and no permanent repositioning. Its FY2026 comparable store sales fell 4%, even as wholesale grew. The ABG video’s 1.8% is an organic growth assumption below ABG’s reported 4.7% growth because it excludes the non-repeatable expansion/mix effect captured in reported growth; it forecasts the existing business, not every dollar of reported expansion.

## Assumption set

The SEC filings are the source of record for historical facts. The provider row above is only a cross-check; it is not pasted into the model as an assumption. “History” means a filed or calculated historical input, “guidance” would mean a management-provided forward input (none is used here), and “judgment” is my forecast choice with its reason stated below.

| Value | Label | Reason |
|---|---|---|
| Wholesale growth: 4.5%, 5.0%, 4.8%, 4.5%, 3.5%; Direct growth: 0.0%, 1.5%, 3.0%, 3.5%, 2.5% (FY2027E–31E) | Judgment | I begin below a normal recovery because total FY2026 revenue was flat and Direct revenue fell 6%, even though wholesale grew 6% reported. The model weights these channel paths by their FY2026 share of total revenue, producing approximately 2.5%, 3.5%, 4.0%, 4.0%, and 3.0% consolidated growth; I would lower the Direct path if traffic, digital sales, or Greater China keeps declining. |
| 43.5%, 44.0%, 44.5%, 45.0%, 45.0% gross margin | Judgment | My starting point is only 60 bps above FY2026’s 42.9%, not a return to FY2024’s 44.6%, because FY2026’s logistics and currency benefits were partly offset by higher NIKE Brand product costs and weaker Converse margin. I allow a gradual recovery as discounting and channel pressure ease; I would hold the margin near 43% if promotions remain necessary to clear product. |
| 60, 110, 160, 210, 210 bps Direct/wholesale channel-normalization margin recovery | Judgment | This is the same company-specific line that produces revenue growth; it also converts the Direct/wholesale mix story into the gross-margin path rather than treating channel mix as a paragraph detached from the model. FY2026 Direct revenue fell 6% while wholesale rose 6% reported; if Direct traffic and digital sales keep falling, I would reduce both the Direct-growth path and this margin recovery. |
| 79.0%, 78.0%, 77.0%, 76.5%, 76.5% S&A ÷ gross profit | Judgment | This ratio was 81.3% in FY2025 and 80.9% in FY2026, so I do not assume a sudden cost reset. I lower it slowly because fixed corporate overhead can be spread over recovering revenue, while preserving demand-creation spending that supports NIKE’s brand; I would not reduce it if wages, severance, or sports-marketing expense keeps growing faster than gross profit. |
| 103.4 inventory days | History | FY2026 inventory ÷ FY2026 cost of sales × 365. |
| 15.6% depreciation ÷ PP&E | History | FY2026 D&A ÷ FY2026 PP&E. D&A remains inside NIKE’s operating-overhead disclosure, so it is added back for cash flow but not deducted a second time in the income statement. |
| 1.47% capex ÷ revenue | History | FY2026 filed additions to PP&E ÷ revenue. |
| 20.3% tax rate | History | FY2026 effective tax rate. |
| Receivables 12.8% of revenue; payables 13.6% of COGS | History | FY2026 balance-sheet ratios. |
| Other assets 24.0% and other liabilities 25.9% of revenue | History | FY2026 balance-sheet ratios; these retain leases, deferred taxes, and other non-core accounts in the simplified model. |
| $715 stock compensation; $2,450 dividends; $150 buybacks annually | Judgment | I use FY2026’s $715 stock compensation, $2.407bn dividends, and only $146m of buybacks as the starting point. I keep dividends slightly above FY2026 but buybacks low because FY2026 free cash flow was weak relative to dividends; I would raise buybacks only after cash from operations recovers and inventory/receivables stop absorbing cash. |
| $400 annual debt repayment | Judgment | NIKE ended FY2026 with $7.942bn of debt, including a $2.0bn current portion. I model a manageable $400m annual reduction instead of assuming all debt is retired quickly or refinanced indefinitely; a new bond issue or a materially different maturity schedule would change this line. |
| $2.0bn cash floor; 6.0% revolver rate | Judgment | The $2.0bn floor is deliberately well below FY2026 cash of $7.563bn, but high enough to avoid making the model depend on daily liquidity. The revolver is a stress-test link, not expected funding in the base case; a draw would tell me the operating assumptions or capital returns are too aggressive. |
| 9.0% cost of equity; 2.5% terminal growth | Judgment | I use 9.0% because NIKE’s earnings are exposed to discretionary consumer demand, foreign exchange, competition, and a still-unproven turnaround, not because it is a risk-free mature staple. I keep terminal growth at 2.5%, below long-run nominal economic growth and far below the near-term recovery, so the terminal value does not assume that a turnaround continues forever. |
| 1,481.0m shares | History | FY2026 diluted weighted-average shares, FY2026 10-K p. 55. |

## Model, checks, and value

`nike_lab10_proforma.py` starts with the FY2026 audited balance sheet and forecasts FY2027E–FY2031E. Cash is calculated from net income, non-cash charges, capital spending, working-capital movements, debt repayment, dividends, and buybacks. If it would go below $2.0bn, the revolver draws; it does not draw in this base case. The script raises an error identifying the year if the statements fail to balance or cash falls below its floor.

The model says **$43.25 per share**; the market says **$35.97 per share at 1:08 PM Eastern on September 24, 2026**, using the same 1,481.0m diluted weighted-average-share denominator in the model. The question is whether NIKE’s recovery in revenue, channel mix, and margin can support the model’s implied value. The market quote was checked at [MarketBeat’s NKE price-history page](https://www.marketbeat.com/stocks/NYSE/NKE/chart/).

## Partner review — complete during the conversation

Do not submit invented partner feedback. Replace the brackets with the actual exchange.

> **Partner’s question in the review:** “How would you do a DCF for Anthropic when it’s growing so fast and its future cash flows are difficult to predict?”
>
> **My answer:** “I would use a multi-stage DCF: model a high-growth period first, gradually fade growth and margins toward a mature level, then test several terminal-value cases instead of treating one number as certain. Because Anthropic’s compute costs and future cash flows are uncertain, I would build in its infrastructure commitments and run conservative sensitivity cases for revenue growth, margins, and terminal growth.”

> **My specific attack on [partner company/ticker]:** “Your [exact assumption] is [number]. The filing shows [specific historical or disclosed comparison]. Why should the model use [number] instead of [alternative], and what would make you change it?”
>
> **Partner’s answer:** [Record their two-sentence answer, including the evidence and what would change the assumption.]

### Prepared attack options for an Anthropic model

Use one only if it matches your partner’s stated assumption, and record their real answer beneath it.

1. **Revenue versus compute commitment:** “Your model assumes Anthropic can grow revenue by **[their rate]** while reaching **[their margin / FCFE]**. Anthropic says its revenue run rate surpassed $30bn, but it also committed more than $100bn over ten years to AWS capacity. Where does that compute commitment appear in your cash-flow or margin assumptions, and what revenue-per-dollar-of-compute result would make you lower the growth or margin forecast?”

2. **Enterprise adoption versus monetization:** “Your model assumes **[their rate]** enterprise revenue growth. Anthropic has public enterprise partnerships and says demand is outpacing its delivery capacity, but a deployment is not necessarily recurring, high-margin revenue. What conversion, retention, and pricing assumptions turn those partnerships into your revenue number, and what evidence would make you reduce them?”
