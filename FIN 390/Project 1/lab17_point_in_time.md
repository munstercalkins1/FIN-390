# Lab 17 — Point-in-Time Audit

## D — The question

**Was each number in my series knowable on the day I would have traded on it,
and may Project 2 use it?**

A number's observation date is not enough to answer that question. The
publication date (represented by an ALFRED vintage) determines whether the
number was in the decision-maker's information set.

## I — App

The runnable app is [asof_app.py](asof_app.py). It downloads current data from
FRED and historical vintages from ALFRED, using only public CSV downloads and
no API key.

Run it from this folder:

```powershell
streamlit run asof_app.py
```

If `streamlit` is not on PATH in the current terminal:

```powershell
& 'C:\Users\munst\AppData\Local\Programs\Python\Python313\python.exe' -m streamlit run asof_app.py
```

The app has four initial series, supports a typed FRED ID, makes separately
cached FRED and ALFRED downloads, shows a current-value chart for each series,
and displays an audit table with last-known dates, later-value counts, and
same-date revision counts. An invalid typed ID produces an error only for that
series; the other series continue to render.

## V — Known-answer validation

With **As known on = 5 October 2026**, the app returned:

| Series | Last date known | Value |
| --- | --- | ---: |
| [BAA](https://fred.stlouisfed.org/series/BAA) | September 2026 | 6.47 |
| [FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS) | September 2026 | 3.75 |
| [DGS10](https://fred.stlouisfed.org/series/DGS10) | 2 October 2026 | 5.28 |
| [MORTGAGE30US](https://fred.stlouisfed.org/series/MORTGAGE30US) | 1 October 2026 | 7.28 |

All four values match the assigned known answer. The live audit also found that
today's data has 16 DGS10 observations and 4 MORTGAGE30US observations after
their respective October 5 last-known dates. These are late observations, not
revisions.

### PAYEMS probe

With `PAYEMS` added and **As known on = 15 January 2025**, the app returned:

| Series | Last date known | Known value | Value today | Revised same dates |
| --- | --- | ---: | ---: | ---: |
| [PAYEMS](https://fred.stlouisfed.org/series/PAYEMS) | December 2024 | 159,536 | 159,044 | 381 |

The nonzero revision count confirms that the app compares an ALFRED vintage
with current FRED data rather than reading today's data twice.

## E — My series data card

**Complete this card after entering the prework FRED ID in the app.** The
series ID was not included in this workspace, so it must not be invented.

| Field | Entry |
| --- | --- |
| Series ID and source link | _Pending prework series ID_ |
| What it measures | _Pending_ |
| Units | _Pending_ |
| Publication lag | _Check the latest date shown by the app as of the last day of the prior month_ |
| Revisions | _Use the app's “Revised same dates” count_ |
| Download date | 29 October 2026 |
| Three values checked against FRED | _Pending manual check_ |

## Learn

**What is a data card?** A compact record of a series' source, definition,
units, timing, revision behavior, download date, and manual verification.

**How does it prevent a leak?** The source/ID and definition prevent a series
substitution; units prevent invalid comparisons; publication lag and vintage
date prevent future information entering the decision; revision status prevents
today's corrected history from masquerading as what was known earlier.

**Why is “cleaned the data” not a data card?** It does not say what changed,
which vintage was used, whether units changed, or whether a transformation
introduced information unavailable at the time. It is a process claim, not
auditable provenance.

## Reflection

An as-known-on date makes the publication lag visible: it shows the last
observation actually available by the decision date, rather than the latest
observation visible today. A backtest using today's values can overstate both
timeliness and apparent predictive value by using observations published later
and revisions made after the historical decision.

## Fresh eyes and Project 2 call

These two items depend on the chosen prework series and the partner's actual
attack. Record the partner's chosen weak field (publication date, revisions, or
units), then support the response with the app's audit row or the FRED source.
Make the Project 2 call as **admit**, **quarantine**, or **reject** and name an
as-of rule plus a condition that would change the call.

## Checkout

Submit links to [asof_app.py](asof_app.py) and this Markdown file after
committing them to the course repository.
