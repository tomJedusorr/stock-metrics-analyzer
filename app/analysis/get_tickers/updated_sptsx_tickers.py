def get_sptsx_tickers():

    import pandas as pd

    # URL of the Wikipedia page containing the TSX Composite Index constituents
    url = "https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index"

    # Read all tables from the Wikipedia page
    tables = pd.read_html(url)

    # Find the table that contains the ticker symbols
    constituents_table = None
    for table in tables:
        if 'Ticker' in table.columns or 'Symbol' in table.columns:
            constituents_table = table
            break

    # Extract and process tickers
    if constituents_table is not None:
        if 'Ticker' in constituents_table.columns:
            tickers = constituents_table['Ticker'].astype(str).tolist()
        elif 'Symbol' in constituents_table.columns:
            tickers = constituents_table['Symbol'].astype(str).tolist()
        else:
            tickers = []
    else:
        tickers = []

    # Replace "." with "-", then add ".TO"
    tsx_tickers = [ticker.strip().upper().replace('.', '-') + ".TO" for ticker in tickers]
    ticker_string = ", ".join(tsx_tickers)

    return ticker_string

if __name__ == "__main__":
    result = get_sptsx_tickers()
    print(result)