"""Lab 15: point-in-time filtering with revisions (standard library only)."""
from __future__ import annotations

from collections import defaultdict
from datetime import date

# Editable inputs -----------------------------------------------------------
DECISION_DATE = "2026-03-31"
TABLE = """row,ticker,month_measured,published_on,index
1,AAA,2026-01,2026-02-10,101.0
2,AAA,2026-02,2026-03-10,104.0
3,AAA,2026-03,2026-04-10,109.0
4,AAA,2026-02,2026-03-25,103.0
5,BBB,2026-01,2026-02-10,98.0
6,BBB,2026-02,2026-03-10,97.0
7,BBB,2026-02,2026-03-10,97.0
8,BBB,2026-03,2026-04-10,92.0
9,CCC,2026-01,2026-02-10,110.0
10,CCC,2026-02,2026-04-05,112.0
11,,2026-02,2026-03-10,99.0
12,CCC,2026-02,2026-03-10,111.0"""


def read_table(text: str) -> list[dict[str, str]]:
    header, *lines = text.strip().splitlines()
    columns = header.split(",")
    return [dict(zip(columns, line.split(","), strict=True)) for line in lines]


def numbers(rows: list[dict[str, str]]) -> str:
    return ", ".join(row["row"] for row in rows) or "none"


def report(rule: str, removed: list[dict[str, str]]) -> None:
    print(f"{rule}: removed {len(removed)} row(s): {numbers(removed)}")


def quarantine_missing_ticker(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    removed = [row for row in rows if not row["ticker"].strip()]
    report("1. Quarantine missing ticker", removed)
    return [row for row in rows if row not in removed]


def remove_exact_duplicates(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str, str, str]] = set()
    kept, removed = [], []
    for row in rows:
        identity = (row["ticker"], row["month_measured"], row["published_on"], row["index"])
        if identity in seen:
            removed.append(row)
        else:
            seen.add(identity)
            kept.append(row)
    report("2. Remove exact duplicate", removed)
    return kept


def remove_after_decision(rows: list[dict[str, str]], decision_date: str) -> list[dict[str, str]]:
    cutoff = date.fromisoformat(decision_date)
    removed = [row for row in rows if date.fromisoformat(row["published_on"]) > cutoff]
    report("3. Remove publication after decision date", removed)
    return [row for row in rows if row not in removed]


def keep_latest_revision(rows: list[dict[str, str]], *, show_report: bool) -> list[dict[str, str]]:
    """Keep the latest publication for each ticker/month; row number breaks a tie."""
    latest: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = (row["ticker"], row["month_measured"])
        candidate = (row["published_on"], int(row["row"]))
        current = latest.get(key)
        if current is None or candidate > (current["published_on"], int(current["row"])):
            latest[key] = row
    kept = [row for row in rows if latest[(row["ticker"], row["month_measured"])] is row]
    if show_report:
        report("4. Keep latest eligible revision", [row for row in rows if row not in kept])
    return kept


def print_panel(title: str, rows: list[dict[str, str]]) -> None:
    print(f"\n{title}")
    print("row  ticker  month measured  published on  index")
    for row in sorted(rows, key=lambda item: (item["ticker"], item["month_measured"])):
        print(f"{row['row']:>3}  {row['ticker']:<6}  {row['month_measured']:<14}  {row['published_on']:<12}  {float(row['index']):>5.1f}")


def signals(rows: list[dict[str, str]]) -> list[tuple[str, str, float]]:
    by_ticker: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_ticker[row["ticker"]].append(row)
    result = []
    for ticker, ticker_rows in sorted(by_ticker.items()):
        monthly = sorted(ticker_rows, key=lambda row: row["month_measured"])
        if len(monthly) >= 2:
            previous, latest = monthly[-2:]
            change = (float(latest["index"]) / float(previous["index"]) - 1) * 100
            result.append((ticker, latest["month_measured"], change))
    return result


def print_signals(label: str, rows: list[dict[str, str]]) -> None:
    print(f"\n{label}")
    for ticker, month, change in signals(rows):
        print(f"{ticker}: {change:+.2f}% (latest month: {month})")


def main() -> None:
    raw = read_table(TABLE)
    print(f"Decision date: {DECISION_DATE}\nStarting rows: {len(raw)}")
    step_1 = quarantine_missing_ticker(raw)
    step_2 = remove_exact_duplicates(step_1)
    step_3 = remove_after_decision(step_2, DECISION_DATE)
    asof_panel = keep_latest_revision(step_3, show_report=True)
    print_panel("As-of panel", asof_panel)
    print_signals("As-of signals", asof_panel)

    # Same valid, nonduplicate rows, but publication dates are ignored.
    naive_panel = keep_latest_revision(step_2, show_report=False)
    print_panel("Naive panel (publication dates ignored)", naive_panel)
    print_signals("Naive signals", naive_panel)


if __name__ == "__main__":
    main()
