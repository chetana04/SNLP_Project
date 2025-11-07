import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
from datetime import datetime

# Import your existing backend logic
from LLM_Powered_Data_Analysis_Agent import (
    crew,
    get_daily_closing_prices,
    format_prices,
)

# ---------------------- Streamlit App ----------------------

st.set_page_config(page_title="Crypto Analysis Crew", layout="wide")

st.title("🧠 Cryptocurrency Market Analysis (Multi-Agent Crew)")

st.markdown(
    """
    This app uses multiple AI agents (CrewAI) to analyze cryptocurrency news and prices,
    then generate a combined market prediction.
    """
)

# Sidebar configuration
st.sidebar.header("🔍 Select Cryptocurrency")
ticker = st.sidebar.text_input("Enter Cryptocurrency Symbol (e.g. BTC, ETH, SOL):", "BTC")

# Button to start analysis
if st.sidebar.button("🚀 Run Analysis"):
    with st.spinner("Fetching data and running AI agents..."):
        try:
            # Fetch and display price data
            df = get_daily_closing_prices(ticker)
            formatted_prices = format_prices(df)

            st.subheader(f"📊 {ticker} - Recent Daily Closing Prices")
            st.text(formatted_prices)

            # Plot the trend
            fig, ax = plt.subplots(figsize=(8, 4))
            df.plot(ax=ax, legend=False)
            plt.title(f"{ticker} Price Trend (Last 60 Days)")
            plt.ylabel("Price (USD)")
            plt.xlabel("Date")
            st.pyplot(fig)

            # Run the Crew AI pipeline
            st.subheader("🤖 Multi-Agent Analysis")
            results = crew.kickoff()

            # Extract outputs from agents
            if "final_output" in results:
                st.markdown("### 🏁 Final Report")
                st.write(results["final_output"])
            else:
                st.warning("No final report generated.")

            # Optionally show detailed logs
            if st.checkbox("Show Detailed Agent Logs"):
                st.json(results, expanded=False)

        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    st.info("👈 Enter a cryptocurrency symbol and click 'Run Analysis' to start.")