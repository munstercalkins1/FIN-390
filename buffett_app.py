"""Streamlit companion for the Buffett 10-K audit skill.

Run: streamlit run buffett_app.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import streamlit as st

SKILL_SCRIPTS = Path(__file__).parent / "buffett-10k-skill" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))
from sec_facts import EdarError, build_audit  # noqa: E402


def display_value(item: dict[str, object], percent: bool = False) -> str:
    value = item["value"]
    if value is None:
        return "not found" if item["tag"] == "not found" else "not known"
    return f"{value:,.1f}%" if percent else f"{value:,.1f}"


def memo_path(ticker: str) -> Path:
    return Path(__file__).parent / f"{ticker.upper()}_buffett_memo.md"


def allowed_numbers(audit: dict[str, object]) -> set[str]:
    """Numbers from the evidence table are the only allowable memo numbers."""
    allowed = set()
    for row in audit["rows"]:
        allowed.update(re.findall(r"\d+(?:\.\d+)?", row["fiscal_year_end"]))
        for key in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "roe", "owner_earnings"):
            value = row[key]["value"]
            if value is not None:
                allowed.add(f"{value:,.1f}")
                allowed.add(f"{value:.1f}")
                allowed.add(f"{value:g}")
                if key == "roe":
                    allowed.add(f"{value:.1f}%")
    allowed.add("15%")
    return allowed


def unprinted_numbers(memo: str, audit: dict[str, object]) -> list[str]:
    memo_without_filing_labels = re.sub(r"\b\d+-K\b", "", memo)
    tokens = re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?%?", memo_without_filing_labels)
    allowed = allowed_numbers(audit)
    return sorted({token for token in tokens if token not in allowed})


@st.cache_data(ttl=3600, show_spinner=False)
def load_audit(ticker: str, user_agent: str) -> dict[str, object]:
    return build_audit(ticker, user_agent)


st.set_page_config(page_title="Buffett 10-K audit", layout="wide")
st.title("Buffett 10-K audit")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    ticker = st.text_input("Ticker", value="COST").upper().strip()
    user_agent = st.text_input("SEC User-Agent (your name and email)", value="Your Name your.email@example.com")

if not ticker or not user_agent.strip():
    st.info("Enter a ticker and an SEC User-Agent before running the audit.")
    st.stop()

try:
    with st.spinner("Downloading SEC 10-K company facts..."):
        audit = load_audit(ticker, user_agent)
except EdarError as error:
    st.error(str(error))
    st.stop()

st.subheader(f"{audit['company']} ({audit['ticker']}) — $ millions")
chart_rows = [
    {"Fiscal year end": row["fiscal_year_end"], "Owner earnings": row["owner_earnings"]["value"], "Net income": row["net_income"]["value"]}
    for row in audit["rows"]
]
st.line_chart(chart_rows, x="Fiscal year end", y=["Owner earnings", "Net income"])

table_rows = []
for row in audit["rows"]:
    table_rows.append({
        "FY end": row["fiscal_year_end"],
        "Revenue": display_value(row["revenue"]), "Revenue tag": row["revenue"]["tag"],
        "Net income": display_value(row["net_income"]), "Net income tag": row["net_income"]["tag"],
        "Operating cash flow": display_value(row["operating_cash_flow"]), "Operating cash flow tag": row["operating_cash_flow"]["tag"],
        "Capital spending": display_value(row["capital_spending"]), "Capital spending tag": row["capital_spending"]["tag"],
        "Equity": display_value(row["equity"]), "Equity tag": row["equity"]["tag"],
        "ROE": display_value(row["roe"], percent=True), "ROE tag": row["roe"]["tag"],
        "Owner earnings": display_value(row["owner_earnings"]), "Owner earnings tag": row["owner_earnings"]["tag"],
    })
st.subheader("Five-year 10-K table")
st.dataframe(table_rows, hide_index=True, width="stretch")

st.subheader("Buffett checks")
st.dataframe([{"Check": label, "Result": result} for label, result in audit["checks"].items()], hide_index=True, width="stretch")

saved_memo = memo_path(ticker)
default_memo = saved_memo.read_text(encoding="utf-8") if saved_memo.exists() else (
    f"# Buffett-style memo — {ticker}\n\nNo memo has been saved for this ticker. Use the skill output only; do not add uncomputed numbers."
)
st.subheader("Buffett-style memo")
memo = st.text_area("Memo", value=default_memo, height=220)
flagged = unprinted_numbers(memo, audit)
if flagged:
    st.error("Numbers not printed by the script: " + ", ".join(flagged))
else:
    st.success("Every number in this memo appears in the script's computed evidence.")
