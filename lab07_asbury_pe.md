# Lab 07 — Comparable-Company Policy and Implied Range

## Reopen and explain

My Week 3 Nike DCF is driven mainly by starting FCFF, the five annual FCFF growth assumptions, WACC, terminal growth, cash, debt, and diluted shares. Its result is especially sensitive to WACC and terminal growth because the terminal value is a large part of enterprise value. My question before researching P/E was: **If two companies have the same earnings per share, why would investors rationally assign different P/E multiples?**

## Define / discover

P/E is price per share divided by earnings per share (EPS). Price per share is the market value of one equity share. Diluted EPS is the earnings attributable to common shareholders divided by diluted weighted-average shares, so it puts a company’s profit on a per-share basis. A P/E multiple says how many dollars of stock price the market assigns to one dollar of that company’s earnings per share. Investor.gov gives the same price/EPS definition and explains that P/E can be compared with a company’s past or other companies’ P/E ratios. [Investor.gov P/E definition](https://www.investor.gov/introduction-investing/investing-basics/glossary/price-earnings-pe-ratio)

Comparing earnings per share makes a price comparison possible even when companies have very different total sizes: the numerator and denominator are both per share. A peer P/E adds a market-based cross-check to my DCF. The DCF asks what my own cash-flow and discount-rate assumptions imply; P/E asks what the market is currently paying for similar companies’ earnings.

It is useful only when the accounting basis, earnings period, capital structure effects, business mix, risk, growth prospects, and profitability are reasonably comparable. A P/E is not meaningful with nonpositive EPS. It can also mislead when earnings contain unusual gains/losses, cyclically high or low margins, or a different expected growth path. A lower P/E therefore does not automatically mean a better investment: it may reflect weaker growth, greater risk, inferior profitability, or temporarily overstated earnings.

## Represent — peer policy before calculation

The relevant business is franchised vehicle retail plus its parts/service and related F&I economics, not merely the broad word “automotive.” Vehicle sales are cyclical and lower-margin, while the service/parts relationship and franchise network affect recurring revenue, margins, and risk.

| Candidate | Decision | Business reason |
|---|---|---|
| AutoNation (AN) | Use | AN operated 325 new-vehicle franchises from 243 U.S. stores at year-end 2024 and sells new/used vehicles, parts and service, and finance and insurance products. That is a close operating match to a franchised retailer. [AutoNation 2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/350698/000035069825000029/an-20241231.htm) |
| Group 1 Automotive (GPI) | Qualify and use | GPI sells and leases new/used vehicles through franchised dealerships and provides maintenance, repair, and parts. It is a strong business match, but its U.K. presence and 2024 U.K. acquisition introduce geographic and integration differences that deserve qualification. [Group 1 2024 overview](https://filecache.investorroom.com/mr5ir_group1new/1540/2024_Group_1_Corporate_Responsibility_Report_FINAL.pdf) |

I retain both peers for the case calculation. I would not choose the peer set based on which one produces the price I prefer.

## Implement and validate

Run the calculator with the same working Python command used for my DCF:

```powershell
python asbury_pe_comparison.py
```

The frozen inputs are Dec. 31, 2024 closing price and FY2024 total GAAP diluted EPS: ABG $243.03 and $21.50; AN $169.84 and $16.92; GPI $421.48 and $36.81. The calculator retains full precision internally and produces:

| Check | Result |
|---|---:|
| AutoNation P/E | 10.037825x |
| Group 1 P/E | 11.450149x |
| Peer median P/E | 10.743987x |
| Asbury peer-implied range | $215.81–$246.18 |
| Asbury at peer median | $231.00 |
| Remove GPI (AN remains) | $215.81 |
| Change from full-peer median estimate | −$15.18 |

One manual check: AN’s P/E is $169.84 / $16.92 = 10.037825x. Applying it to ABG’s $21.50 EPS gives $215.81 per ABG share.

## Evolve and reflect

Before viewing the leave-one-out output, I predicted that removing GPI would lower the implied ABG price because GPI has the higher P/E. The result confirms this: the estimate moves from the two-peer median estimate of $231.00 to AN’s $215.81, a $15.18 decline. With only AN remaining there is no minimum-to-maximum peer range; it is one reference estimate, not evidence of a valuation interval.

P/E measures the market price paid for each dollar of EPS. AN belongs because its franchised dealership and after-sales business closely match the target. GPI also belongs but needs qualification for its geographic footprint and acquisition-related differences. This comparison does not prove ABG is fairly valued: it transfers peer market pricing to ABG and depends on the peer policy and the assumption that the earnings, risk, growth, and accounting are comparable.

## GitHub submission

Repository: [munstercalkins1/FIN-390](https://github.com/munstercalkins1/FIN-390)

Files: [lab07_asbury_pe.md](https://github.com/munstercalkins1/FIN-390/blob/main/lab07_asbury_pe.md) and [asbury_pe_comparison.py](https://github.com/munstercalkins1/FIN-390/blob/main/asbury_pe_comparison.py)
