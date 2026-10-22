"""Streamlit interface for the Lab 15 portfolio engine.

Run: streamlit run app.py
"""

from __future__ import annotations

from io import StringIO

import streamlit as st

from portfolio import (MERIDIAN_ASSETS, MERIDIAN_CORRELATIONS, MERIDIAN_OBJECTIVE,
                       MERIDIAN_RESERVE_ELIGIBLE, MERIDIAN_RESERVE_MINIMUM,
                       MERIDIAN_RETURNS, MERIDIAN_VOLATILITIES,
                       estimate_from_prices, search_lowest_risk_mix)


def read_uploaded_estimates(uploaded_file, last_36_months):
    text = uploaded_file.getvalue().decode("utf-8-sig")
    return estimate_from_prices(StringIO(text), last_36_months)


def show_answer(title, answer, assets):
    st.subheader(title)
    if answer is None:
        st.warning("No mix meets the objective.")
        return
    st.dataframe({"Asset": assets, "Weight": [answer["weights"][asset] for asset in assets]},
                 hide_index=True, column_config={"Weight": st.column_config.NumberColumn(format="%.0%%")})
    one, two, three = st.columns(3)
    one.metric("Expected return", f"{answer['return']:.2%}")
    two.metric("Volatility", f"{answer['volatility']:.2%}")
    three.metric("Reserve-eligible", f"{answer['reserve_weight']:.2%}")


st.set_page_config(page_title="Lowest-risk portfolio mix", layout="wide")
st.title("Lowest-risk portfolio mix")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    st.header("Controls")
    objective = st.number_input("Objective expected return (%)", value=MERIDIAN_OBJECTIVE * 100, step=0.1) / 100
    reserve_minimum = st.number_input("Reserve minimum (%)", value=MERIDIAN_RESERVE_MINIMUM * 100, step=0.1) / 100
    uploaded_file = st.file_uploader("Upload prices.csv", type="csv")
    last_36 = st.toggle("Use only the last 36 months", value=False)

try:
    if uploaded_file is None:
        loaded_returns = MERIDIAN_RETURNS.copy()
        loaded_volatilities = MERIDIAN_VOLATILITIES.copy()
        loaded_correlations = MERIDIAN_CORRELATIONS
        source_label = "Meridian inputs"
    else:
        loaded_returns, loaded_volatilities, loaded_correlations = read_uploaded_estimates(uploaded_file, last_36)
        source_label = "CSV historical estimates (not forecasts)"
except ValueError as error:
    st.error(f"Could not read the CSV: {error}")
    st.stop()

assets = list(loaded_returns)
st.write(f"**Source:** {source_label}. Returns are annual estimates.")
st.subheader("Expected-return estimates")
edited_returns = {}
for asset in assets:
    edited_returns[asset] = st.number_input(f"{asset} return (%)", value=float(loaded_returns[asset] * 100), step=0.1, key=f"return_{asset}") / 100

st.subheader("Reserve eligibility")
reserve_eligible = set()
for asset in assets:
    default = asset in MERIDIAN_RESERVE_ELIGIBLE if uploaded_file is None else False
    if st.checkbox(asset, value=default, key=f"reserve_{asset}"):
        reserve_eligible.add(asset)

loaded_answer = search_lowest_risk_mix(loaded_returns, loaded_volatilities, loaded_correlations,
                                       objective, reserve_eligible, reserve_minimum)
edited_answer = search_lowest_risk_mix(edited_returns, loaded_volatilities, loaded_correlations,
                                       objective, reserve_eligible, reserve_minimum)

left, right = st.columns(2)
with left:
    show_answer("Answer for inputs as loaded", loaded_answer, assets)
with right:
    show_answer("Lowest-risk mix with edited estimates", edited_answer, assets)
    if loaded_answer is not None and edited_answer is not None:
        largest_change = max(abs(edited_answer["weights"][asset] - loaded_answer["weights"][asset]) for asset in assets)
        st.info(f"Largest weight change: {largest_change:.0%}")
