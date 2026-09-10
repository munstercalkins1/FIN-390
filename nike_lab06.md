# Lab 06 - Nike, Inc. (NYSE: NKE)

## Source table and model inputs

| Input | Value used | Unit | As-of date | Source and locator |
|---|---:|---|---|---|
| Starting FCFF | 2,144.15 | USD millions | FY ended May 31, 2026 | [Nike FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/320187/000032018726000088/nke-20260531.htm), Consolidated Statements of Cash Flows: operating cash flow 2,868.00 + after-tax net interest income of -39.85 [(-50.00) x (1 - 792/3,900)] - capex 684.00. |
| Growth, Year 1 | 3.0% | annual | Forecast from FY2026 | Student forecast: modest recovery after FY2026 revenue of $46.398B, using Item 7 MD&A and recent history. |
| Growth, Year 2 | 5.0% | annual | Forecast from FY2026 | Student forecast; same basis as Year 1. |
| Growth, Year 3 | 6.0% | annual | Forecast from FY2026 | Student forecast; same basis as Year 1. |
| Growth, Year 4 | 5.0% | annual | Forecast from FY2026 | Student forecast; same basis as Year 1. |
| Growth, Year 5 | 4.0% | annual | Forecast from FY2026 | Student forecast; same basis as Year 1. |
| WACC | 10.0% | annual | September 10, 2026 | Estimate, not copied: 4.5% + 1.3 x 5.0% = 11.0% cost of equity; 6.0% x (1 - 25.0%) = 4.5% after-tax debt cost; 85% equity / 15% debt mix gives about 10.0%. |
| Terminal growth | 3.0% | perpetual annual | September 10, 2026 | Conservative long-run economic assumption. CBO projects real GDP growth around 1.8% after 2026 and PCE inflation settling at 2.0% by 2030; 3.0% is below a simple nominal-growth combination. [CBO outlook](https://www.cbo.gov/publication/62105) |
| Non-operating cash | 9,027.00 | USD millions | May 31, 2026 | Nike 10-K, Consolidated Balance Sheets: cash and equivalents 7,563 plus short-term investments 1,464. |
| Debt | 7,942.00 | USD millions | May 31, 2026 | Nike 10-K, Consolidated Balance Sheets: current portion of long-term debt 2,000 plus long-term debt 5,942. Operating lease liabilities excluded because operating lease expense is already reflected in operating cash flow. |
| Diluted shares | 1,481.00 | millions | FY ended May 31, 2026 | Nike 10-K, Consolidated Statements of Income, diluted weighted-average common shares outstanding. |
| Today's NKE price | 37.35 | USD per share | September 10, 2026, 15:59:59 | [Investing.com historical price page](https://ca.investing.com/equities/nike-historical-data), displayed close. |

## Results and reasonableness

`python dcf.py` produces a base-case value of **$23.5038 per diluted share**, compared with the September 10 price of **$37.35**. That is 62.9% of the price, so it is inside the 0.5x-2.0x reasonableness band.

| WACC \ terminal growth | 2.0% | 3.0% | 4.0% |
|---|---:|---:|---:|
| 9.0% | $24.2769 | $27.3340 | $31.6138 |
| 10.0% | $21.2932 | $23.5038 | $26.4511 |
| 11.0% | $18.9738 | $20.6320 | $22.7639 |

With the starting FCFF, WACC, terminal growth, cash, debt, diluted shares, and five-year horizon held fixed, the September 10 price implies a **+11.6474 percentage-point uniform addition** to each explicit annual FCFF growth rate. The reverse-DCF search range was set to -5.0% through +20.0%; it was widened from the initial +10.0% upper bound because the target price was not reachable there.

The input I distrust most is starting FCFF: FY2026 operating cash flow included a $1.207B increase in accounts receivable and therefore may not represent normalized free cash flow.

## Conditional call

**Watch-defer.** Initiate if the growth shift implied by the market price falls below my explicit forecast path - a price below about **$23.50** with all other assumptions held fixed - or if Nike provides sourced evidence that its operating-cash-flow conversion and operating margin are recovering. Otherwise, defer; monitor next quarter's operating margin and cash conversion.

The reverse-DCF shift is a description of what the target price implies with all other inputs held fixed, not proof of mispricing.

## GitHub submission

Repository: [munstercalkins1/FIN-390](https://github.com/munstercalkins1/FIN-390)

Files for Lab 06: [nike_lab06.md](https://github.com/munstercalkins1/FIN-390/blob/main/nike_lab06.md) and [dcf.py](https://github.com/munstercalkins1/FIN-390/blob/main/dcf.py)
