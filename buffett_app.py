"""Lab 18 Streamlit panel: Buffett, Graham, and Burry on the same 10-K facts."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import streamlit as st

SKILL_SCRIPTS = Path(__file__).parent / "buffett-10k-skill" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))
from sec_facts import EdarError, build_audit  # noqa: E402
from panel_analysis import checks, memos, panel_verdicts  # noqa: E402


def display(item: dict[str, object], percent: bool = False) -> str:
    value = item["value"]
    if value is None:
        return "not found" if item["tag"] == "not found" else "not known"
    return f"{value:,.2f}%" if percent else f"{value:,.2f}"


def allowed_numbers(audit: dict[str, object], check_rows: list[dict[str, str]]) -> set[str]:
    allowed: set[str] = set()
    metric_keys = ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "liabilities", "assets_current", "liabilities_current", "roe", "owner_earnings", "current_ratio", "liabilities_to_equity")
    for row in audit["rows"]:
        allowed.update(re.findall(r"\d+(?:\.\d+)?", row["fiscal_year_end"]))
        for key in metric_keys:
            value = row[key]["value"]
            if value is not None:
                allowed.update((f"{value:,.2f}", f"{value:.2f}", f"{value:g}"))
                if key == "roe":
                    allowed.add(f"{value:.2f}%")
    for row in check_rows:
        allowed.update(re.findall(r"\d+(?:\.\d+)?", row["Check"]))
    return allowed


def unprinted_numbers(memo: str, audit: dict[str, object], check_rows: list[dict[str, str]]) -> list[str]:
    memo = re.sub(r"\b\d+-K\b", "", memo)
    tokens = re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?%?", memo)
    allowed = allowed_numbers(audit, check_rows)
    return sorted({token for token in tokens if token not in allowed})


@st.cache_data(ttl=3600, show_spinner=False)
def load_audit(ticker: str, user_agent: str) -> dict[str, object]:
    return build_audit(ticker, user_agent)


st.set_page_config(page_title="Lab 18 investor panel", layout="wide")
st.title("Lab 18 — three-investor 10-K panel")
st.caption("The same SEC 10-K facts; separate mechanical screens. Learning demonstration, not investment advice.")
st.subheader("The investors")
investors = st.columns(3)
with investors[0]:
    st.markdown("### Warren Buffett\n**Business quality**\n\nROE and owner earnings across five annual 10-K periods.")
with investors[1]:
    st.markdown("### Benjamin Graham\n**Financial cushion**\n\nCurrent ratio and net-income record; the threshold is adjustable for the probe.")
with investors[2]:
    st.markdown("### Michael Burry\n**Cash and leverage**\n\nOperating-cash-flow conversion and latest liabilities relative to equity.")

with st.sidebar:
    ticker = st.text_input("Ticker", value="COST").upper().strip()
    user_agent = st.text_input("SEC User-Agent (your name and email)", value="")
    graham_threshold = st.number_input("Graham current-ratio threshold", min_value=0.1, value=1.0, step=0.1)

if not ticker or not user_agent.strip():
    st.info("Enter a ticker and SEC User-Agent before running the panel.")
    st.stop()

try:
    with st.spinner("Downloading SEC 10-K company facts..."):
        audit = load_audit(ticker, user_agent)
except EdarError as error:
    st.error(str(error))
    st.stop()

st.subheader(f"{audit['company']} ({audit['ticker']}) — $ millions")
st.line_chart(
    [{"Fiscal year end": row["fiscal_year_end"], "Owner earnings": row["owner_earnings"]["value"], "Net income": row["net_income"]["value"]} for row in audit["rows"]],
    x="Fiscal year end", y=["Owner earnings", "Net income"],
)
table_rows = []
for row in audit["rows"]:
    table_rows.append({
        "FY end": row["fiscal_year_end"], "Revenue": display(row["revenue"]), "Net income": display(row["net_income"]),
        "Operating cash flow": display(row["operating_cash_flow"]), "Capital spending": display(row["capital_spending"]),
        "Equity": display(row["equity"]), "Liabilities": display(row["liabilities"]),
        "Assets current": display(row["assets_current"]), "Liabilities current": display(row["liabilities_current"]),
        "ROE": display(row["roe"], percent=True), "Owner earnings": display(row["owner_earnings"]),
        "Current ratio": display(row["current_ratio"]), "Liabilities / equity": display(row["liabilities_to_equity"]),
    })
st.dataframe(table_rows, hide_index=True, width="stretch")
with st.expander("Selected XBRL tags"):
    tag_keys = ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "liabilities", "assets_current", "liabilities_current", "roe", "owner_earnings", "current_ratio", "liabilities_to_equity")
    st.dataframe([
        {"FY end": row["fiscal_year_end"], **{key: row[key]["tag"] for key in tag_keys}}
        for row in audit["rows"]
    ], hide_index=True, width="stretch")

st.header("Panel")
check_rows = checks(audit, graham_threshold)
st.dataframe([{"Investor": row["Investor"], "Check": row["Check"], ticker: row["Result"]} for row in check_rows], hide_index=True, width="stretch")
verdicts = panel_verdicts(check_rows)
st.dataframe([{"Investor": investor, "Verdict": value} for investor, value in verdicts.items()], hide_index=True, width="stretch")

st.subheader("Three memos")
memo_values = memos(audit, graham_threshold)
columns = st.columns(3)
edited_memos = {}
for column, investor in zip(columns, ("Buffett", "Graham", "Burry")):
    with column:
        edited_memos[investor] = st.text_area(f"{investor} memo", value=memo_values[investor], height=220)

flagged = {investor: unprinted_numbers(memo, audit, check_rows) for investor, memo in edited_memos.items()}
if any(flagged.values()):
    st.error("Unprinted memo numbers: " + "; ".join(f"{investor}: {', '.join(values)}" for investor, values in flagged.items() if values))
else:
    st.success("Every number in all three memos appears in printed evidence or a printed panel rule.")

with st.expander("Sources"):
    st.markdown("[FAskills](https://github.com/CinderZhang/FAskills) · [Graham defensive screen](https://ownerscorecard.com/tests/defensive/) · [Burry research background](https://hedgefundalpha.com/michael-burry-bio/) · [Streamlit dataframe docs](https://docs.streamlit.io/develop/concepts/design/dataframes) · [SEC developer resources](https://www.sec.gov/about/developer-resources)")

st.divider()
st.subheader("Arrive with")
st.markdown("- Your Lab 18 skill and app matching COST\n- Your Lab 18 chat\n- Your partner\n- The ticker of the largest company inside one of your Project 2 funds (the prework)")
st.subheader("Thursday merit checkout")
st.caption("Project 2 studio • 75 minutes")
st.dataframe([
    {"Minutes": "0–8", "Anchor": "Opener"}, {"Minutes": "8–33", "Anchor": "Build the panel"},
    {"Minutes": "33–43", "Anchor": "V and probe"}, {"Minutes": "43–50", "Anchor": "Your company"},
    {"Minutes": "50–56", "Anchor": "Explain the code"}, {"Minutes": "56–62", "Anchor": "Bull and bear"},
    {"Minutes": "62–70", "Anchor": "Decision and learn"}, {"Minutes": "70–75", "Anchor": "Reflect and checkout"},
], hide_index=True, width="stretch")
