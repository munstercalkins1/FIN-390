# Lab 08 — Your Company, Your Comparables

## Company, date, and research question

Target: Nike, Inc. (NYSE: NKE). Comparison date: **September 10, 2026**. My question is: *What would one NKE share be worth at defensible peer P/E multiples, and how does that compare with my Week 3 DCF?*

Nike earns money by designing, developing, marketing, and selling athletic footwear, apparel, equipment, accessories, and services through both NIKE Direct (owned stores and digital platforms) and wholesale accounts. [Nike FY2026 Form 10-K, Item 1](https://www.sec.gov/Archives/edgar/data/320187/000032018726000088/nke-20260531.htm) I need a listed operating company with branded technical athletic apparel/footwear economics, positive annual GAAP diluted EPS, and earnings public by September 10, 2026.

## Peer policy and candidates

**Policy written before naming candidates:** Admit a listed operating company only if it sells branded athletic footwear/apparel through a meaningful direct-to-consumer and/or wholesale channel, has positive annual GAAP diluted EPS reported publicly by the comparison date, and has a business model sufficiently similar to Nike’s branded-product economics. Qualify material differences in scale, product mix, geography, channel mix, or growth. Reject a company when it fails these business criteria, has nonpositive annual GAAP diluted EPS, lacks a same-date price, or has annual earnings unavailable by the comparison date. I will not choose a peer based on the implied price.

| Candidate | Business evidence and difference | Annual EPS available by Sept. 10? | Decision |
|---|---|---|---|
| lululemon athletica (NASDAQ: LULU) | Lululemon sells technical athletic apparel, footwear, and accessories and operates an omni-channel retail model. [FY2025 Form 10-K, Item 1](https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm) A key difference is its much smaller, more vertically retail-led model and concentration in women’s apparel, versus Nike’s much larger global footwear, wholesale, and brand portfolio. | FY ended Feb. 1, 2026; GAAP diluted EPS **$13.26**; 10-K filed Mar. 17, 2026. [EPS note](https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm), [filing date](https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/0001397187-26-000020-index.html) | **Use, with qualification.** It meets the product and direct-channel criteria, but the business-mix and scale differences limit this to a one-peer reference. |
| Under Armour (NYSE: UAA) | Under Armour reported both wholesale and direct-to-consumer net sales, so it is a reasonable business-model candidate. [FY2026 Form 10-K, revenue recognition](https://www.sec.gov/Archives/edgar/data/1336917/000133691726000073/ua-20260331.htm) Its smaller scale and current turnaround are important differences. | FY ended Mar. 31, 2026; GAAP diluted loss per share **($1.16)**; 10-K filed May 19, 2026. [FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1336917/000133691726000073/ua-20260331.htm), [filing date](https://www.sec.gov/Archives/edgar/data/1336917/000133691726000073/0001336917-26-000073-index.html) | **Exclude.** Its annual GAAP EPS is negative, so its P/E is not meaningful. |

## Source and input table

All prices are regular-session closing prices on September 10, 2026; annual EPS is GAAP diluted EPS, not adjusted EPS. The historical-price pages were opened to match the same trading date: [NKE](https://chartexchange.com/symbol/nyse-nke/historical/), [LULU](https://chartexchange.com/symbol/nasdaq-lulu/historical/), and [UAA](https://stockanalysis.com/stocks/uaa/history/).

| Company | Close | Annual GAAP diluted EPS | Fiscal period / publication date | Source locator | Treatment |
|---|---:|---:|---|---|---|
| Nike (NKE), target | $36.62 | $2.10 | FY ended May 31, 2026 / filed July 15, 2026 | [10-K EPS table](https://www.sec.gov/Archives/edgar/data/320187/000032018726000088/nke-20260531.htm); [filing detail](https://www.sec.gov/Archives/edgar/data/320187/000032018726000088/0000320187-26-000088-index.html) | Target |
| lululemon (LULU) | $96.88 | $13.26 | FY ended Feb. 1, 2026 / filed Mar. 17, 2026 | [10-K EPS note](https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm) | Use, qualified |
| Under Armour (UAA), candidate | $4.97 | ($1.16) | FY ended Mar. 31, 2026 / filed May 19, 2026 | [10-K diluted loss per share](https://www.sec.gov/Archives/edgar/data/1336917/000133691726000073/ua-20260331.htm) | Exclude: P/E not meaningful |

I corrected a date mismatch in my older Week 3 source table: $37.35 was NKE’s September 9 close. The matched September 10 close is $36.62. The DCF intrinsic-value calculation itself does not change because its valuation inputs remain the same; this correction only changes the market-price comparison.

## Implementation and validation

Run:

```powershell
python nike_pe_comparison.py
```

The calculator includes only LULU because it is the sole admitted peer. It calculates LULU’s P/E as $96.88 / $13.26 = **7.306184x**. Applying that unrounded multiple to Nike’s $2.10 FY2026 GAAP diluted EPS gives a **$15.34 reference estimate**. This is not a range: one usable peer cannot provide a minimum-to-maximum peer interval.

I predicted that removing LULU would leave no estimate, because it is the only admitted usable peer. The leave-one-out output confirms it: remove LULU → **no estimate (no peers remain)**. This is a loss of comparison information, not a reason to add an unsuitable peer or to reject LULU for its result.

## DCF comparison and skeptical review

| Method | Value / result | What it says | Key limitation |
|---|---:|---|---|
| Market price on Sept. 10 | $36.62 | Current market reference | Not an intrinsic-value estimate |
| Week 3 DCF | $23.50 per share | Value from my FCFF, growth, WACC, terminal-growth, cash, debt, and shares assumptions | Terminal value and the cash-flow recovery path materially affect it |
| P/E comparison | $15.34 reference estimate | Nike valued at LULU’s annual GAAP P/E | One qualified peer; LULU’s scale, channel mix, and product mix differ materially |

**Provisional call: Watch-defer.** Both valuation approaches sit below the matched market price, but I will not average them. The P/E result is only a one-peer reference and the DCF depends on an uncertain Nike recovery path. I would reconsider if Nike demonstrates a sustained recovery in revenue, margin, and cash conversion, or if additional defensible, positive-EPS peers support a materially different P/E reference.

Skeptical-colleague criticism I accept: the weakest supported assumption is treating Lululemon’s high-margin, more vertically integrated athletic-apparel economics as a direct valuation reference for Nike’s much larger footwear and wholesale business. I accept it because the sources document that difference; the result is therefore a qualified reference rather than a valuation range. I reject averaging the $15.34 P/E reference and $23.50 DCF because they answer different questions and the peer evidence is thin.

Question that could change my decision: **Can I document a durable recovery in Nike’s wholesale/direct sales mix and operating margin that makes my FCFF growth path more credible?** That evidence would change the DCF support; a second defensible positive-EPS peer could also improve the market cross-check.

## Reflection

Lululemon belongs, with qualification, because it is a branded technical athletic-products operator with an omni-channel model, but it differs in scale, product emphasis, and vertical retail exposure. Under Armour was investigated and excluded because its reported annual GAAP EPS is negative; a price divided by a negative earnings number is not a meaningful P/E valuation multiple. The comparison adds a market-based earnings cross-check to the DCF, but it does not prove that Nike is fairly valued. My defensible P/E conclusion is a **$15.34 one-peer reference**, not a range, and my conclusion remains **watch-defer** rather than initiate.

## GitHub checkout

Repository: [munstercalkins1/FIN-390](https://github.com/munstercalkins1/FIN-390)

Files: [lab08_nike_pe.md](https://github.com/munstercalkins1/FIN-390/blob/main/lab08_nike_pe.md) and [nike_pe_comparison.py](https://github.com/munstercalkins1/FIN-390/blob/main/nike_pe_comparison.py)
