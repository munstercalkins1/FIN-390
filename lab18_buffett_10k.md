# Lab 18 — Buffett 10-K Skill

## D — The question

**Can an investor's philosophy become a skill an AI runs the same way every
time—every number computed by code from the 10-K, with the judgment left to the
model?**

Yes, for a defined screen. The repeatable part is data selection and arithmetic;
the non-repeatable part is the short business-quality judgment drawn only from
that evidence.

## Skill and app

The reusable skill is in [buffett-10k-skill](buffett-10k-skill/SKILL.md). It
contains a narrowly scoped `SKILL.md` and the bundled deterministic SEC script
at [sec_facts.py](buffett-10k-skill/scripts/sec_facts.py). The Streamlit
companion is [buffett_app.py](buffett_app.py), and the generated COST judgment
is [COST_buffett_memo.md](COST_buffett_memo.md).

Run the script with a real SEC-compliant User-Agent containing your name and
email:

```powershell
python buffett-10k-skill/scripts/sec_facts.py COST --user-agent "Your Name your.email@example.com" --json COST_facts.json
```

Run the app:

```powershell
streamlit run buffett_app.py
```

The app charts owner earnings and net income; shows values, XBRL tags, and
computed checks; displays the memo; and flags memo numbers absent from the
computed table.

## V — Costco known answer

The live SEC EDGAR run matched the required COST values, in $ millions:

| FY end | Revenue | Net income | Operating cash flow | Capital spending | Equity | ROE | Owner earnings |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2022-08-28 | 226,954 | 5,844 | 7,392 | 3,891 | 20,642 | 28.3% | 3,501 |
| 2023-09-03 | 242,290 | 6,292 | 11,068 | 4,323 | 25,058 | 25.1% | 6,745 |
| 2024-09-01 | 254,453 | 7,367 | 11,339 | 4,710 | 23,622 | 31.2% | 6,629 |
| 2025-08-31 | 275,235 | 8,099 | 13,335 | 5,498 | 29,164 | 27.8% | 7,837 |
| 2026-08-30 | 303,154 | 9,226 | 15,817 | 6,435 | 35,803 | 25.8% | 9,382 |

All three computed checks are **pass**: ROE is at least 15% every year, owner
earnings are positive every year, and owner earnings grew from the first year
to the last.

### JPMorgan probe

The JPM run leaves capital spending as **not found** and owner earnings as
**not found**. Therefore, “Owner earnings positive every year” and “Owner
earnings grew, first year to last” are **not known**, not estimated. The memo
cannot judge JPM's owner earnings using this screen.

### Memo-number probe

The app accepts the saved COST memo because every financial number occurs in
the computed evidence. Adding `40.0%` produces: **“Numbers not printed by the
script: 40.0%.”**

## Explain the code

`metric_value()` is the conversion point from raw EDGAR facts to one table
cell. It considers only the allowed XBRL tags for that metric, retrieves USD
facts, chooses the latest filed matching 10-K fact for the fiscal-year-end date,
and divides dollars by one million. If no allowed fact survives those rules, it
returns `value: None` and `tag: not found`. `build_audit()` then computes ROE
only when equity is positive and computes owner earnings only when both cash
flow inputs exist.

## Decision

I trust the Costco verdict as a reproducible business-quality screen because
the five years, tags, arithmetic, and pass/fail rules come from code using SEC
10-K facts. I would not treat it as a complete investment recommendation until
I separately assess the durability of the business and valuation.

## Learn and reflect

An agent skill is a folder whose name and description help the AI decide when
it applies; the rest of `SKILL.md` is loaded only when needed, keeping unrelated
instructions out of ordinary tasks. This skill makes 10-K-only fact selection,
tag priority, latest-filing choice, calculations, and missing-data treatment
identical on every run. The model is left to write a qualitative verdict from
the computed evidence only.

The numbers belong in code because arithmetic and data-selection rules can be
rerun and audited; a model should not recreate financial facts from prose.
`Not found` is better than an estimate because it preserves uncertainty and
prevents a missing input from becoming a fabricated pass/fail result.

## Checkout

Submit GitHub links to this file, `buffett-10k-skill/SKILL.md`,
`buffett-10k-skill/scripts/sec_facts.py`, `buffett_app.py`, and
`COST_buffett_memo.md`.

## Lab 19 panel extension

Startup command: `streamlit run buffett_app.py`  
Observed error before the server was started: `ERR_CONNECTION_REFUSED (102)` at
`http://localhost:8502/`.

The panel keeps the original 10-K selection rules and adds AssetsCurrent,
LiabilitiesCurrent, and Liabilities. It computes current ratio as assets current
divided by liabilities current and liabilities-to-equity as liabilities divided
by equity. The COST regression test checks the required panel result: Buffett
3/3 pass; Graham 2/3 with current ratio 1.06 failing the default 2.0 threshold;
and Burry 2/2 pass. Missing inputs remain not known.
