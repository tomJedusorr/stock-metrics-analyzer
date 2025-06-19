import numpy as np
from .average_info import arith_average
from scipy.stats import norm
from ..hist_data.ticker_prices import get_price
from ..economic_info.risk_free import get_rf
from datetime import date
from dateutil.relativedelta import relativedelta
from yahooquery import Ticker


def stand_var(frame, freq):

    stand_dev_dict = {}
    list_tick = frame['adjclose'].columns

    for t in list_tick: 
        values = frame['overallReturn'][t].dropna() - 1

        if freq == "m":
            stand_dev_dict[t] = np.std(values, ddof=1) * np.sqrt(21)
        elif freq in ["y", "a"]:
            stand_dev_dict[t] = np.std(values, ddof=1) * np.sqrt(252)
        else:
            stand_dev_dict[t] = np.std(values, ddof=1)

    return stand_dev_dict



def down_dev(frame, freq):

    down_dev_dict = {}
    list_tick = frame['adjclose'].columns

    for t in list_tick: 
        values = frame['overallReturn'][t].dropna() - 1
        returns_neg = values[values < 0.0]

        if freq == "m":
            down_dev_dict[t] = np.std(returns_neg, ddof=1) * np.sqrt(21)
        elif freq in ['y', 'a']:
            down_dev_dict[t] = np.std(returns_neg, ddof=1) * np.sqrt(252)
        else:
            down_dev_dict[t] = np.std(returns_neg, ddof=1)

    return down_dev_dict



# We are adjusting the sharpe ratio by removing the risk-free rate
def sharpe_adj(frame, freq):

    sharpe_dict = {}
    list_tick = frame['adjclose'].columns

    avg = arith_average(frame, freq)
    stand = stand_var(frame, freq)

    for t in list_tick:
        sharpe_dict[t] = avg.get(t) / stand.get(t)

    return sharpe_dict



# We are adjusting the sortino ratio by removing the risk-free rate
def sortino_adj(frame, freq):

    sortino_dict = {}
    list_tick = frame['adjclose'].columns

    avg = arith_average(frame, freq)
    down = down_dev(frame, freq)

    for t in list_tick:
        sortino_dict[t] = avg.get(t) / down.get(t)

    return sortino_dict



# More accurate when measured with daily data
def max_draw(frame):

    max_draw_dict = {}
    list_tick = frame['adjclose'].columns

    for t in list_tick:
        returns = frame['overallReturn'][t].dropna()
        cum_re = returns.cumprod()

        # Returns a serie with all the maximum point
        peak = cum_re.cummax()

        drawdowns = (cum_re - peak) / peak
        max_drawdown = drawdowns.min()
        max_draw_dict[t] = max_drawdown

    return max_draw_dict



# It returns the max negative return on a "confidence"%
def varisk(frame, freq, confidence='95'):

    var_dict = {}
    list_tick = frame['adjclose'].columns

    avg = arith_average(frame, freq)
    stand = stand_var(frame, freq)

    for t in list_tick:
        mu = avg.get(t)
        sigma = stand.get(t)

        if confidence == '95':
            z_score = norm.ppf(0.05) # around -1,645

        elif confidence == '97.5':
            z_score = norm.ppf(0.025) # around -1,96
        
        else:
            z_score = norm.ppf(0.01) # around -2,326

        var_dict[t] = mu + (z_score * sigma)

    return var_dict



# The Conditionnal VaR returns the average negative returns beyond the 95% confidence
def cvarisk(frame, freq, confidence='95'):

    cvar_dict = {}
    list_tick = frame['adjclose'].columns

    if confidence == '95':
        alpha = 5
    
    elif confidence == '97.5':
        alpha = 2.5

    else:
        alpha = 1

    for t in list_tick:
        returns = frame['overallReturn'][t].dropna() - 1
        var = np.percentile(returns, alpha)

        if freq == "m":
            cvar_dict[t] = np.mean(returns[returns <= var]) * 21
        elif freq in ["y", "a"]:
            cvar_dict[t] = np.mean(returns[returns <= var]) * 252
        else:
            cvar_dict[t] = np.mean(returns[returns <= var])

    return cvar_dict



# Retrieve a beta calculated upon a 5-year monthly analysis from yahooquery
def beta(frame):

    beta_dict = {}
    list_tick = frame['adjclose'].columns

    path = Ticker(list_tick).summary_detail

    for t in list_tick:
        try:
            beta_dict[t] = path.get(t, {}).get('beta', np.nan)
        except:
            beta_dict[t] = np.nan

    return beta_dict



# Could be used in the future
def beta_dailyframe(frame):

    beta_dict = {}

    # We store the main info of indexes on a dict
    index_tick = {".TO": '^GSPTSE', ".PA": '^FCHI', ".DE": '^GDAXI', ".MI": 'FTSEMIB.MI', "": '^GSPC'}

    t_col = frame['dailyReturn'].columns

    for t in t_col:

        # 'FTSEMIB.MI' being the only one w/o a '^'
        if t.find("^") == -1 and t != 'FTSEMIB.MI':

            r_col = frame['dailyReturn'][t].dropna()[1:]
            size_s = len(r_col)

            for key, values in index_tick.items():

                if t.find(key) > -1:

                    mkt_returns = frame['dailyReturn'][values].dropna()[1:]
                    size_i = len(mkt_returns)

                    # We determine which size to base upon
                    if size_s >= size_i:

                        r_col_adj = r_col[:size_i]
                        mkt_returns_adj = mkt_returns

                    else:

                        mkt_returns_adj = mkt_returns[:size_s]
                        r_col_adj = r_col

                elif key == "":
                    
                    mkt_returns = frame['dailyReturn'][values].dropna()[1:]
                    size_i = len(mkt_returns)

                    if size_s >= size_i:

                        r_col_adj = r_col[:size_i]
                        mkt_returns_adj = mkt_returns

                    else:

                        mkt_returns_adj = mkt_returns[:size_s]
                        r_col_adj = r_col


            cov_matrix = np.cov(mkt_returns_adj, r_col_adj)

            # Covariance by itself is equal to variance
            beta_dict[t] = cov_matrix[0, 1] / cov_matrix[1, 1]

    return beta_dict
#



# Capital asset pricing model, first developed by William F.Sharpe in 1964
# Considering the frequency and the lookback period of the Beta for the avg return and rf
def capm(frame_1, frame_2, freq):

    capm_dict = {}
    index_tick = {".TO": '^GSPTSE', ".PA": '^FCHI', ".DE": '^GDAXI', ".MI": 'FTSEMIB.MI'}
    list_tick = frame_1['overallReturn'].columns

    # We take monthly as th standard frequency like the Beta
    overall_r = arith_average(frame_2, "m")
    overall_b = beta(frame_1)

    rf = get_rf('m')

    for t in list_tick:
        beta_r = overall_b.get(t)
        try:
            # Find the appropriate index
            matched_index = next((index for key, index in index_tick.items() if key in t), '^GSPC')

            mkt_avg = overall_r.get(matched_index)
            capm_monthly = rf + beta_r * (mkt_avg - rf)

            # Scale CAPM by frequency
            if freq == "d":
                capm_dict[t] = capm_monthly / 21
            elif freq == "m":
                capm_dict[t] = capm_monthly
            else:
                capm_dict[t] = capm_monthly * 12

        except Exception as e:
            capm_dict[t] = np.nan

    return capm_dict



# The Alpha represents the difference between the expected return (CAPM) versus the real return
def alpha(frame_1, frame_2, freq):

    alpha_dict = {}
    list_tick = frame_1['overallReturn'].columns

    overall_c = capm(frame_1, frame_2, freq)
    avg_d_return = arith_average(frame_1, freq)

    for t in list_tick:
        avg_return = avg_d_return.get(t)

        try:
            alpha_dict[t] = avg_return - overall_c.get(t)
        except:
            alpha_dict[t] = np.nan

    return alpha_dict



# We are adjusting the treynor ratio by removing the risk-free rate
# Similar than the SHarpe, but with Beta as denominator
def treynor_adj(frame, freq):

    treynor_dict = {}
    list_tick = frame['overallReturn'].columns

    overall_avg = arith_average(frame, freq)
    overall_beta = beta(frame)

    for t in list_tick:
        try:
            treynor_monthly = overall_avg.get(t) / overall_beta.get(t)

            if freq == "d":
                treynor_dict[t] = treynor_monthly / 21

            elif freq == "m":
                treynor_dict[t] = treynor_monthly

            else:
                treynor_dict[t] = treynor_monthly * 12
        except:
            treynor_dict[t] = np.nan

    return treynor_dict