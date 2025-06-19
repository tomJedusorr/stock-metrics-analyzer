from .analysis.get_tickers.convert_tickers import tick_to_str
from .analysis.analytic_func.additional_info import pos_p, extreme_return
from .analysis.analytic_func.average_info import arith_average, geom_avg, ema_avg
from .analysis.analytic_func.risk_info import stand_var, sharpe_adj, sortino_adj, down_dev, max_draw, beta, treynor_adj, capm, cvarisk, varisk, alpha
from .analysis.fundam_info.main_info import get_fundam_info
from .analysis.hist_data.ticker_prices import get_price
import pandas as pd
from yahooquery import Ticker
from datetime import date
from dateutil.relativedelta import relativedelta


# Beta, Alpha, Capm, Treynor are thos taking a "ticker(s)" as parameters
# All the others take the entire dataframe

# Format for ticker = "AAPL, META, ..." or "AAPL; META; ..."
# Format for start dates = "None (takes a 10y ago one)" or "yyyy-mm-dd"
# Format for end dates = "None (takes the current date)" or "yyyy-mm-dd"
# Format for frequency = "m", "d", or ("a" or "y")

def mainf(ticker, attributes, start=None, end=None, freq="a"):
    
    dataf = get_price(ticker, start, end, freq="d")
    dataff = get_price(ticker, start, end, freq="d", include_benchmarks=True)
    san_tick = dataf['adjclose'].columns

    conf_levels = ['95', '97.5', '99']
    result = {}

    # Prepare storage only for selected attributes
    calculated = {}

    # === Conditional calculations ===
    if any(a in attributes for a in ["arith_avg"]):
        calculated['arith_avg'] = arith_average(dataf, freq)
    if any(a in attributes for a in ["geom_avg"]):
        calculated['geom_avg'] = geom_avg(dataf, freq)
    if "ema_avg" in attributes:
        calculated['ema_avg'] = ema_avg(dataf, freq)
    if "stand_var" in attributes:
        calculated['stand_var'] = stand_var(dataf, freq)
    if "sharpe" in attributes:
        calculated['sharpe'] = sharpe_adj(dataf, freq)
    if "sortino" in attributes:
        calculated['sortino'] = sortino_adj(dataf, freq)
    if "down_dev" in attributes:
        calculated['down_dev'] = down_dev(dataf, freq)
    if "max_draw" in attributes:
        calculated['max_draw'] = max_draw(dataf)
    if "beta" in attributes:
        calculated['beta'] = beta(dataf)
    if "treynor" in attributes:
        calculated['treynor'] = treynor_adj(dataf, freq)
    if "capm" in attributes:
        calculated['capm'] = capm(dataf, dataff, freq)
    if "alpha" in attributes:
        calculated['alpha'] = alpha(dataf, dataff, freq)
    if "pos_prob" in attributes:
        calculated['pos_prob'] = pos_p(dataf)
    if "min_return" in attributes:
        calculated['min_return'] = extreme_return(dataf, freq, 'min')
    if "max_return" in attributes:
        calculated['max_return'] = extreme_return(dataf, freq, 'max')
    if any(a.startswith("cvar_") for a in attributes):
        for level in conf_levels:
            if f"cvar_{level}" in attributes:
                calculated[f"cvar_{level}"] = cvarisk(dataf, freq, level)
    if any(a.startswith("var_") for a in attributes):
        for level in conf_levels:
            if f"var_{level}" in attributes:
                calculated[f"var_{level}"] = varisk(dataf, freq, level)

    # === Fundamentals ===
    fundamental_map = {
        "market_cap": "marketCap",
        "trailing_pe": "trailingPE",
        "forward_pe": "forwardPE",
        "enterpriseValue": "enterpriseValue",
        "sector": "sector",
        "div_yield": "dividendYield",
        "float_shares": "floatShares",
        "price_book": "priceToBook"
    }

    selected_fundamentals = {
        key: get_fundam_info(dataf, api_field)
        for key, api_field in fundamental_map.items()
        if key in attributes
    }

    # === Assemble result ===
    for t in san_tick:
        result[t] = {}

        for attr in attributes:
            if attr in calculated:
                result[t][attr] = calculated[attr].get(t)
            elif attr in selected_fundamentals:
                result[t][attr] = selected_fundamentals[attr].get(t)
            elif attr == "real_start":
                result[t]["real_start"] = dataf['adjclose'][t].dropna().index[0].strftime('%Y-%m-%d')
            elif attr == "real_end":
                result[t]["real_end"] = dataf['adjclose'][t].dropna().index[-1].strftime('%Y-%m-%d')

    return pd.DataFrame(result)