"""Lab 17 Streamlit app: inspect FRED data as it was known on a past date.

Run with: streamlit run asof_app.py
"""

from __future__ import annotations

import csv
from datetime import date
from io import StringIO
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen

import altair as alt
import streamlit as st


SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}


class DownloadError(RuntimeError):
    """A series could not be downloaded or parsed as a FRED-style CSV."""


def parse_csv(text: str, series_id: str) -> list[tuple[date, float]]:
    """Parse FRED/ALFRED graph CSV and omit FRED's '.' missing observations."""
    reader = csv.DictReader(StringIO(text))
    if not reader.fieldnames or len(reader.fieldnames) < 2 or "observation_date" not in reader.fieldnames:
        raise DownloadError(f"{series_id}: FRED did not return a recognizable CSV.")
    value_column = next(name for name in reader.fieldnames if name != "observation_date")
    values = []
    for row in reader:
        raw_value = (row.get(value_column) or "").strip()
        if raw_value in {"", "."}:
            continue
        try:
            values.append((date.fromisoformat(row["observation_date"]), float(raw_value)))
        except (TypeError, ValueError) as error:
            raise DownloadError(f"{series_id}: could not read an observation in the download.") from error
    if not values:
        raise DownloadError(f"{series_id}: the download contained no numeric observations.")
    return sorted(values)


def fetch(url: str, series_id: str) -> list[tuple[date, float]]:
    try:
        with urlopen(url, timeout=30) as response:
            text = response.read().decode("utf-8-sig")
    except (HTTPError, URLError, TimeoutError) as error:
        raise DownloadError(f"{series_id}: download failed ({error}).") from error
    return parse_csv(text, series_id)


@st.cache_data(ttl=3600, show_spinner=False)
def download_today(series_id: str) -> list[tuple[date, float]]:
    """Download the values shown by FRED today; cached for one hour."""
    series_id = series_id.strip().upper()
    return fetch(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={quote(series_id)}", series_id)


@st.cache_data(ttl=3600, show_spinner=False)
def download_as_known_on(series_id: str, vintage_date: str) -> list[tuple[date, float]]:
    """Download ALFRED's vintage available on vintage_date; cached for one hour."""
    series_id = series_id.strip().upper()
    url = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id="
    url += f"{quote(series_id)}&vintage_date={quote(vintage_date)}"
    return fetch(url, series_id)


def last_on_or_before(values: list[tuple[date, float]], when: date) -> tuple[date, float] | None:
    eligible = [point for point in values if point[0] <= when]
    return eligible[-1] if eligible else None


def summary_row(series_id: str, known: list[tuple[date, float]], today_values: list[tuple[date, float]], as_of: date) -> dict[str, object]:
    """Build one audit row: latest known vintage, current vintage, lag, revisions."""
    last_known = last_on_or_before(known, as_of)
    if last_known is None:
        raise DownloadError(f"{series_id}: no numeric observation was known by {as_of:%Y-%m-%d}.")
    last_today = today_values[-1]
    known_by_date = dict(known)
    today_by_date = dict(today_values)
    later_count = sum(observation_date > last_known[0] for observation_date in today_by_date)
    revised_count = sum(
        observation_date in today_by_date and today_by_date[observation_date] != value
        for observation_date, value in known_by_date.items()
        if observation_date <= last_known[0]
    )
    return {
        "Series": f"https://fred.stlouisfed.org/series/{series_id}",
        "Known date": last_known[0].isoformat(),
        "Known value": last_known[1],
        "Today date": last_today[0].isoformat(),
        "Today value": last_today[1],
        "Values later": later_count,
        "Revised same dates": revised_count,
    }


st.set_page_config(page_title="Point-in-time rate audit", layout="wide")
st.title("Point-in-time rate audit")
st.caption("Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    st.header("Controls")
    selected = st.multiselect(
        "Series IDs",
        options=list(SERIES),
        default=list(SERIES),
        format_func=lambda item: f"{item} — {SERIES[item]}",
    )
    typed_id = st.text_input("Add another FRED series ID", placeholder="Example: PAYEMS").strip().upper()
    start_date = st.date_input("Chart start date", value=date(2020, 1, 1))
    as_of_date = st.date_input("As known on", value=date.today())

all_ids = selected + ([typed_id] if typed_id and typed_id not in selected else [])
if not all_ids:
    st.info("Choose at least one series ID.")
    st.stop()

audit_rows = []
chart_by_date: dict[date, dict[str, object]] = {}
last_known_labels = []
plotted_ids = []
for series_id in all_ids:
    try:
        today_values = download_today(series_id)
        known_values = download_as_known_on(series_id, as_of_date.isoformat())
        row = summary_row(series_id, known_values, today_values, as_of_date)
    except DownloadError as error:
        st.error(str(error))
        continue

    chart_values = [(observation_date, value) for observation_date, value in today_values if observation_date >= start_date]
    if not chart_values:
        st.warning(f"{series_id}: no current observations on or after {start_date:%Y-%m-%d}.")
        continue
    st.subheader(f"{series_id} — {SERIES.get(series_id, 'Additional FRED series')}")
    st.line_chart([{"date": observation_date, series_id: value} for observation_date, value in chart_values], x="date", y=series_id)
    st.caption(f"Last date known on {as_of_date:%d %B %Y}: {row['Known date']} — {row['Known value']:g}")
    for observation_date, value in chart_values:
        chart_by_date.setdefault(observation_date, {"date": observation_date})[series_id] = value
    plotted_ids.append(series_id)
    last_known_labels.append(f"{series_id}: {row['Known date']} — {row['Known value']:g}")
    audit_rows.append(row)

if plotted_ids:
    st.subheader("Current series values")
    combined_points = [
        {"date": row["date"].isoformat(), "series": series_id, "value": row[series_id]}
        for row in chart_by_date.values()
        for series_id in plotted_ids
        if series_id in row
    ]
    combined_chart = (
        alt.Chart(alt.Data(values=combined_points))
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("value:Q", title="Rate"),
            color=alt.Color(
                "series:N",
                title="Series",
                scale=alt.Scale(range=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]),
                legend=alt.Legend(orient="top"),
            ),
            tooltip=[alt.Tooltip("series:N", title="Series"), alt.Tooltip("date:T", title="Date"), alt.Tooltip("value:Q", title="Value", format=".2f")],
        )
        .properties(height=400)
    )
    st.altair_chart(combined_chart, width="stretch")
    st.caption("Combined chart: each selected series has its own color; use the legend to identify it.")

if audit_rows:
    st.subheader("As-known-on audit")
    st.dataframe(
        audit_rows,
        hide_index=True,
        column_config={
            "Series": st.column_config.LinkColumn("Series", display_text=r".*/series/(.*)"),
            "Known value": st.column_config.NumberColumn(format="%.2f"),
            "Today value": st.column_config.NumberColumn(format="%.2f"),
        },
        width="stretch",
    )
