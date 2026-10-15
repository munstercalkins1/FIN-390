# Lab 13 — Meridian Foundation Reserve

## Statement types and IPS map

An investment policy statement (IPS) records a client's objectives, constraints, governance rules, and unresolved decisions so that an investment process can be evaluated against the client's actual mandate.

| Statement | Type | Why / IPS role |
|---|---|---|
| S1 | Hard constraint | A seven-year horizon and annual rebalancing set the investment time frame and implementation schedule. |
| S2 | Objective | CPI + 4% net of costs over rolling five-year periods is the return objective. |
| S3 | Hard constraint | The quarterly payout and one-year cash/daily-liquid government reserve are a spending and liquidity requirement. |
| S4 | Preference | The 60/40 benchmark is a comparison reference, not a stated portfolio limit or objective. |
| S5 | Hard constraint | Long-only and the bans on borrowing, shorts, and derivatives are explicit implementation limits. |
| S6 | Hard constraint | No single issuer above 8% is a concentration limit. |
| S7 | Hard constraint | Turnover above 25% needs committee approval, a governance/implementation limit. |
| S8 | Hard constraint | At least 90% redeemable within five business days is an explicit liquidity limit. |
| S9 | Unverifiable promise | The 10% calendar-year-loss wording provides neither a measurement convention nor a breach rule, so it cannot be tested. |
| S10 | Missing | It supplies no sector, ESG, tax, or home-bias preference and, crucially, no optimization criterion. |

## Checker and verification

The checker is [mandate.py](mandate.py). Run it with:

```powershell
python mandate.py
```

It computes the reserve minimum as 3.0% and produces the specified A/B/C results: A passes every checkable rule, B fails three, and C fails one. It deliberately prints `requires CIO clarification` for the calendar-year-loss statement rather than treating S9 as a limit. Acme bonds and stock are aggregated as one issuer.

### Long-only probe

I temporarily changed A's Cash weight to -2 and Global equity index fund to 64, then reran the file. A's lowest weight was -2.0 and failed long-only; its reserve weight remained 10.0 and no other rule failed. I then restored the original A inputs.

### Self-quiz

**Question:** Why does the issuer check add the Acme bond and stock weights instead of checking each holding independently?  
**My answer before explanation:** The mandate applies the 8% limit to one company's securities together. Thus B has 5% + 4% = 9% Acme exposure and fails, while C has 8% and passes.

### Candidate D: attack on the checker

Candidate D is 10% Cash and 90% Treasury bills (all other holdings are 0%). It passes every rule that `mandate.py` checks.

The objection holds: this almost entirely cash-equivalent portfolio could reasonably be rejected because it is unlikely to pursue CPI + 4% net of costs over rolling five-year periods. S2, the return objective, decides the objection; the checker tests constraints but does not test whether a portfolio is designed to meet that objective.

If reviewing a partner's same D, I would cite S2 for the same reason: passing liquidity and concentration floors does not demonstrate a credible path to the stated real return objective.

## Question for the CIO before optimization

**Question:** What precise risk measure, valuation convention, and breach action make S9's “no calendar-year loss greater than 10%” a binding rule (for example, total return measured at calendar year-end, with what action after a breach)?

**Answer that changes the portfolio:** If it is a hard ex-ante total-return limit, the optimizer needs an explicit downside-risk constraint and would likely hold less equity/risk than if it is only a monitoring threshold or an ex-post governance trigger.

## Reflection

A portfolio can pass every checkable rule yet still be wrong because rules such as liquidity, issuer concentration, and long-only are floors and prohibitions—not proof it can meet the client's real-return objective, horizon, spending needs, or unstated risk tolerance. Candidate D demonstrates that gap.

The type I was least sure of was S4. I classified it as a preference/reference benchmark because the CIO did not say it is a tracking target, a required allocation, or an optimization objective; if it is meant to control active risk, the CIO must say so.
