import numpy as np

# When unspecify, all avg returns take dividends and split into account
def arith_average(frame, freq):

    arith_avg_dict = {}
    list_tick = frame['adjclose'].columns

    for t in list_tick:
        if freq == "m":
            arith_avg_dict[t] = (np.nanmean(frame['overallReturn'][t]) - 1) * 21
        elif freq in ["y", "a"]:
            arith_avg_dict[t] = (np.nanmean(frame['overallReturn'][t]) - 1) * 252
        else:
            arith_avg_dict[t] = (np.nanmean(frame['overallReturn'][t]) - 1)

    return arith_avg_dict



def geom_avg(frame, freq):

    geom_avg_dict = {}
    list_tick = frame['adjclose'].columns

    for t in list_tick:
        values = frame['adjclose'][t].dropna()[1:]
        size = len(values) - 1

        if freq == "m":
            geom_avg_dict[t] = ((values.iloc[-1] / values.iloc[0]) ** (1 / (size / 21))) - 1
        elif freq in ["y", "a"]:
            geom_avg_dict[t] = ((values.iloc[-1] / values.iloc[0]) ** (1 / (size / 252))) - 1
        else:
            geom_avg_dict[t] = ((values.iloc[-1] / values.iloc[0]) ** (1 / (size))) - 1

    return geom_avg_dict



def ema_avg(frame, freq):

    ema_avg_dict = {}
    list_tick = frame['adjclose'].columns

    for t in list_tick:
        values = frame['overallReturn'][t].dropna()[1:] - 1
        size = len(values)

        # Here lies the logic to get an accurate span
        # For example, a span of 200 gives the first weight a value of "(2 / (200 + 1)) = 0.995%"
        if freq == "d":  # Daily
            if size >= 200:
                span = 200  # long-term
            elif size >= 100:
                span = 100  # medium-term
            elif size >= 50:
                span = 50
            else:
                span = 20  # short-term default

        elif freq == "m":  # Monthly
            if size >= 36:
                span = 36  # 3-year smoothing
            elif size >= 24:
                span = 24
            elif size >= 12:
                span = 12  # 1 year
            else:
                span = 6   # half-year default

        elif freq in ["y", "a"]:  # Yearly
            if size >= 10:
                span = 10  # decade smoothing
            elif size >= 5:
                span = 5
            else:
                span = 3  # 3-year minimal smoothing

        if freq == "m":
            ema_avg_dict[t] = (values.ewm(span, adjust=False).mean().iloc[-1]) * 21
        elif freq == "d":
            ema_avg_dict[t] = values.ewm(span, adjust=False).mean().iloc[-1]
        else:
            ema_avg_dict[t] = (values.ewm(span, adjust=False).mean().iloc[-1]) * 252

    return ema_avg_dict
