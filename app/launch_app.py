import streamlit as st
import datetime
import io
import os
import sys

attribute_choices = [
    "arith_avg", "geom_avg", "ema_avg", "stand_var", "sharpe", "sortino", "down_dev",
    "max_draw", "beta", "treynor", "capm", "alpha", "cvar_95", "cvar_975", "cvar_99",
    "var_95", "var_975", "var_99", "pos_prob", "min_return", "max_return",
    "market_cap", "trailing_pe", "forward_pe", "enterpriseValue", "sector", 
    "div_yield", "float_shares", "price_book", "real_start", "real_end"
    ]

# Get the directory of this script
current_dir = os.path.dirname(__file__)

# Go up one level to the project root
project_root = os.path.abspath(os.path.join(current_dir, '..'))

# Add the project root to sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.mainflow_app import mainf

# Streamlit Web App
st.title("Get Relevant Stock Metrics")

# User Inputs
tickers_input = st.text_input("Enter Stock Tickers:")

MIN_DATE = datetime.date(1900, 1, 1)
MAX_DATE = datetime.date.today()

start_date = st.date_input("Start Date", value=datetime.date(2000, 1, 1), min_value=MIN_DATE, max_value=MAX_DATE)
end_date = st.date_input("End Date", value=MAX_DATE, min_value=MIN_DATE, max_value=MAX_DATE)

frequency = st.selectbox("Select Frequency", ["d", "m", "y"], index=1)

selected_metrics = st.multiselect("Select the analysis metrics you'd like to compute:", attribute_choices)

st.write(f"Selected Date Range: {start_date} to {end_date}")

if st.button("Analyze Stocks"):
    with st.spinner("Fetching data..."):
        results_df = mainf(tickers_input, selected_metrics, start_date, end_date, frequency)
        st.dataframe(results_df)

        # Provide CSV download option
        csv_file = results_df.to_csv(index=True).encode('utf-8')
        st.download_button("Download Results as CSV", csv_file, "stock_analysis.csv", "text/csv")

        # Excel Download (in-memory, no disk write)
        excel_buffer = io.BytesIO()
        results_df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        st.download_button(
            label="Download Results as Excel",
            data=excel_buffer,
            file_name="stock_analysis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )