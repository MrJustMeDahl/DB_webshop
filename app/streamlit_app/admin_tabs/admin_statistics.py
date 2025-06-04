import streamlit as st
from database.db_functionality.statistics_functionality import (
    fetch_monthly_revenue,
    fetch_avg_customer_revenue,
    fetch_avg_order_value,
    fetch_avg_review_length
)

def display_statistics():
    st.header("1. Revenue per month")
    monthly_df = fetch_monthly_revenue()
    st.line_chart(monthly_df.set_index("date")["total_revenue"])

    st.header("2. Average revenue per customer")
    st.metric("", f"{fetch_avg_customer_revenue():,.2f} $")

    st.header("3. Average order value")
    st.metric("", f"{fetch_avg_order_value():,.2f} $")

    st.header("4. Average review length")
    st.metric("", f"{fetch_avg_review_length():,.1f} words")

