# All based on daily data so far
def pos_p(frame):

    pos_dict = {}
    list_tick = frame['adjclose'].columns

    for t in list_tick:
        returns = frame['overallReturn'][t].dropna() - 1
        size = len(returns)
        returns_adj_p = returns[returns > 0]
        size_pos = len(returns_adj_p)

        pos_dict[t] = size_pos / size

    return pos_dict



def extreme_return(frame, freq, edge):

    extreme_r_dict = {}
    list_tick = frame['adjclose'].columns

    for t in list_tick:
        returns = frame['overallReturn'][t].dropna() - 1

        if edge == "min":
            if freq == "m":
                extreme_r_dict[t] = returns.min() * 21
            elif freq == "d":
                extreme_r_dict[t] = returns.min()
            else:
                extreme_r_dict[t] = returns.min() * 252

        else:
            if freq == "m":
                extreme_r_dict[t] = returns.max() * 21
            elif freq == "d":
                extreme_r_dict[t] = returns.max()
            else:
                extreme_r_dict[t] = returns.max() * 252

    return extreme_r_dict