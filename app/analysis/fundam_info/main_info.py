import numpy as np
from yahooquery import Ticker

# List of potential fundam info:
# 'enterpriseValue'
# 'trailingPE'
# 'marketCap'
# 'forwardPE'
# 'sector'
# 'dividendYield'
# 'floatShares'
# 'priceToBook'

def get_fundam_info(frame, info):

    fundam_info_dict = {}
    list_tick = frame['adjclose'].columns
    call = Ticker(list_tick)

    infos_1 = call.summary_profile
    infos_2 = call.key_stats
    infos_3 = call.summary_detail

    for t in list_tick:
        if info == 'sector':
            try:
                fundam_info_dict[t] = infos_1.get(t, {}).get(info, np.nan)
            except:
                fundam_info_dict[t] = np.nan
        
        elif info in ['enterpriseValue', 'priceToBook', 'floatShares']:
            try:
                fundam_info_dict[t] = infos_2.get(t, {}).get(info, np.nan)
            except:
                fundam_info_dict[t] = np.nan
        else:
            try:
                fundam_info_dict[t] = infos_3.get(t, {}).get(info, np.nan)
            except:
                fundam_info_dict[t] = np.nan

    return fundam_info_dict