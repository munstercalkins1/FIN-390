---
name: buffett-10k-audit
description: Compute a five-year Buffett-style business-quality audit from SEC EDGAR 10-K company facts when evaluating a U.S. public-company ticker; use for repeatable fundamentals, not price valuation.
---

# Buffett 10-K audit

Use `scripts/sec_facts.py` to create the evidence before writing any judgment.
The script is the source of every numerical claim: it uses 10-K company facts
only, retains the latest filed fact for a repeated period, and prints both the
value and the XBRL tag selected.

## Workflow

1. Ask for or use a ticker and a SEC-compliant User-Agent that includes the
   user's name and email. Do not invent either.
2. Run the script for the ticker. Preserve `not found` and `not known` exactly;
   do not substitute an estimate or a nearby XBRL tag.
3. Use the script's three computed checks and printed table as the sole numeric
   evidence for a short memo. Judge business quality only: `own the business`,
   `watch it`, or `pass`. Do not discuss price, market capitalization, or stock
   performance.
4. Save the memo as `<TICKER>_buffett_memo.md`. Before finalizing it, make sure
   every number in the memo appears in the script output.

## Command

```powershell
python scripts/sec_facts.py COST --user-agent "Your Name your.email@example.com" --json COST_facts.json
```

The Streamlit companion at `../buffett_app.py` uses the same script functions
and flags memo numbers that are absent from the computed evidence.
