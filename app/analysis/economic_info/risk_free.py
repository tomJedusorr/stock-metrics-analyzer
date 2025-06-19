from fredapi import Fred

def get_rf(freq='a'):

    fred = Fred(api_key='acb2d179d51fb6dde4b7a8e3a4839ce3')

    rate_series = fred.get_series('DGS10')  # DGS10 = 10-Year Constant Maturity Rate

    # Drop missing values
    rate_series = rate_series.dropna()

    # Get the most recent value
    latest_rate = rate_series.iloc[-1] / 100 

    if freq == 'm':
        latest_rate = ((1 + latest_rate) ** (1/12)) - 1
    elif freq == 'd':
        latest_rate = ((1 + latest_rate) ** (1/252)) - 1
        
    return latest_rate

if __name__ == "__main__":
    result = get_rf()
    print(result)