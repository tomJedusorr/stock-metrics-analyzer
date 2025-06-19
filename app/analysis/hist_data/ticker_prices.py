import pandas as pd
from ..get_tickers.convert_tickers import tick_to_str
from yahooquery import Ticker
from datetime import date
from dateutil.relativedelta import relativedelta

def get_price(ticker, start_date=None, end_date=None, freq="d", include_benchmarks=False):

    if start_date is None:
        start_date = (date.today() - relativedelta(years=10)).strftime('%Y-%m-%d')

    list_adj = tick_to_str(ticker)

    # Add benchmarks only if needed
    if include_benchmarks:
        benchmark_tickers = ['^GSPTSE', '^FCHI', '^GDAXI', 'FTSEMIB.MI', '^FTSE', '^GSPC']
        list_adj_ind = list_adj + benchmark_tickers
    else:
        list_adj_ind = list_adj

    ticker_list = Ticker(list_adj_ind)

    # Download data
    if end_date is None:
        ticker_list_adj = ticker_list.history(start=start_date).reset_index()
    else:
        ticker_list_adj = ticker_list.history(start=start_date, end=end_date).reset_index()

    if 'dividends' in ticker_list_adj.columns:
    
        # Standardize date format
        ticker_list_adj['dateAdj'] = pd.to_datetime(ticker_list_adj['date'], utc=True).dt.tz_localize(None)

        # Pivot to get daily adjclose and dividends
        adjclose = ticker_list_adj.pivot(index='dateAdj', columns='symbol', values='adjclose')
        dividends = ticker_list_adj.pivot(index='dateAdj', columns='symbol', values='dividends')

        # --- Resample prices ---
        if freq == "w":
            adjclose = adjclose.resample("WE").last()
            dividends = dividends.resample("WE").sum()
        elif freq == "m":
            adjclose = adjclose.resample("ME").last()
            dividends = dividends.resample("ME").sum()
        elif freq in ["y", "a"]:
            adjclose = adjclose.resample("YE").last()
            dividends = dividends.resample("YE").sum()

        # Ensure dividends align perfectly with resampled adjclose
        dividends = dividends.reindex(adjclose.index).fillna(0)

        # Calculate returns (1 + r format)
        overall_return = adjclose.pct_change(fill_method=None) + 1

        # Build final DataFrame with MultiIndex
        final_dtf = pd.concat([adjclose, dividends, overall_return], axis=1, keys=['adjclose', 'dividends', 'overallReturn'])
    
    else:
        # Standardize date format
        ticker_list_adj['dateAdj'] = pd.to_datetime(ticker_list_adj['date'], utc=True).dt.tz_localize(None)

        # Pivot to get daily adjclose and dividends
        adjclose = ticker_list_adj.pivot(index='dateAdj', columns='symbol', values='adjclose')

        # --- Resample prices ---
        if freq == "w":
            adjclose = adjclose.resample("WE").last()
        elif freq == "m":
            adjclose = adjclose.resample("ME").last()
        elif freq in ["y", "a"]:
            adjclose = adjclose.resample("YE").last()

        # Calculate returns (1 + r format)
        overall_return = adjclose.pct_change(fill_method=None) + 1

        # Build final DataFrame with MultiIndex
        final_dtf = pd.concat([adjclose, overall_return], axis=1, keys=['adjclose', 'overallReturn'])

    return final_dtf