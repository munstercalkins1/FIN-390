# Lab 15 — Point-in-Time Filter

## D — The question

**On the day I would have traded, what did the data actually say—and how much
of what I see now came later?**

The decision date is **31 March 2026**. A month measured describes the period
the value is about; its publication date determines when the value could have
been used. Therefore, a March value published in April cannot support a March
31 trade, even though it describes March.

## I — Implementation

The runnable implementation is [asof.py](asof.py). It uses the standard
library only. Its editable inputs are at the top: `TABLE` and `DECISION_DATE`.

Run:

```powershell
python asof.py
```

If the current PowerShell window has not refreshed its PATH, run:

```powershell
& 'C:\Users\munst\AppData\Local\Programs\Python\Python313\python.exe' asof.py
```

The code applies the rules in this order:

1. Quarantine blank tickers.
2. Remove exact duplicate records.
3. Remove records published after the decision date.
4. Within each ticker/month, retain the latest remaining publication—the
   eligible revision.

`signals()` sorts each ticker's remaining months, compares the latest index to
the preceding month's index, and calculates `(latest / previous - 1) * 100`.
The naive comparison performs rules 1, 2, and 4 but deliberately skips rule 3.

## V — Known-answer proof

### Row funnel

| Funnel step | Rows removed |
| --- | --- |
| Quarantined: no ticker | 11 |
| Exact duplicate | 7 |
| Published after 31 March | 3, 8, 10 |
| Older vintage replaced by a revision | 2 |

### As-of panel

| Row | Ticker | Month measured | Published on | Index |
| ---: | --- | --- | --- | ---: |
| 1 | AAA | 2026-01 | 2026-02-10 | 101.0 |
| 4 | AAA | 2026-02 | 2026-03-25 | 103.0 |
| 5 | BBB | 2026-01 | 2026-02-10 | 98.0 |
| 6 | BBB | 2026-02 | 2026-03-10 | 97.0 |
| 9 | CCC | 2026-01 | 2026-02-10 | 110.0 |
| 12 | CCC | 2026-02 | 2026-03-10 | 111.0 |

### Signals

| Ticker | As-of signal | Naive signal |
| --- | --- | --- |
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | −1.02% (February) | −5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February) |

For the April 15 check, change `DECISION_DATE` in `asof.py` to `"2026-04-15"`
and run it again. Rows 3, 8, and 10 are then eligible; the filtered signals
become the naive signals ticker-for-ticker.

## Learn

**1. What is look-ahead bias?** It is using information in a historical test
before that information was available in real time.

**2. How does it work here?** Event time is the month measured; publication
time is when the index became available. A revision replaces a prior vintage
only if that revision itself was published by the decision date. A correct
backtest must preserve all three facts.

**3. AAA explanation.** The naive AAA signal is +5.83% because it compares
February's latest index, 103.0, with March's 109.0. But 109.0 was published on
April 10. On March 31, the newest knowable AAA month was February and the
signal was only +1.98% (103.0 versus January's 101.0).

## Reflect

Rule 3, the publication-date rule, removed row 3—the row that mattered most
for AAA's apparent performance. A naive backtest would claim that a trader had
the +5.83% AAA March signal on March 31. That exaggerates the information set
available at the decision and can make a strategy appear more predictive and
profitable than it could have been in live trading.

## Checkout

Submit links to this Markdown file and [asof.py](asof.py) after committing them
to the course repository.
