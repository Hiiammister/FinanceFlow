import streamlit as st
from core.schema import init_db

st.set_page_config(page_title="FinanceFlow", layout="wide")

init_db()

st.title("FinanceFlow")
st.write("Use the pages in the sidebar to manage transactions, budgets, reports, and AI insights.")
st.info("Tip: Start with **Add Transaction**, then check **Dashboard** and **AI Insights**.")
