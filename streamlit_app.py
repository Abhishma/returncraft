
from __future__ import annotations
from pathlib import Path
import streamlit as st

from returncraft.pipeline import review_case
from returncraft.utils import load_json

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

st.set_page_config(page_title="Returncraft", layout="wide")
st.title("Returncraft")
st.caption("Policy-grounded returns and refund exception handling with abstention and escalation.")

example = st.sidebar.selectbox("Example case", ["example_case_001.json", "example_case_003.json"])
case = load_json(DATA_DIR / example)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Case input")
    st.json(case)

with col2:
    st.subheader("Review output")
    review = review_case(case)
    st.json(review)
    if review["status"] == "abstained":
        st.warning("System abstained because the case is not safely grounded.")
    else:
        st.success("Review-ready output generated.")
    if review["escalation_required"]:
        st.info("Escalation required.")

st.markdown("---")
st.subheader("Portfolio interpretation")
if review["status"] == "abstained":
    st.write("This refusal is a trust feature. The system does not recommend action without grounded policy support.")
else:
    st.write("This repo is decision support under policy and uncertainty, not a refund automation bot.")
