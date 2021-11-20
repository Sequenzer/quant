import pandas as pd

def SMA(data, n):
    return pd.Series(data).rolling(n).mean()

def moving_average(data, lenght, offset):
    return pd.Series(data).rolling(lenght).mean().shift(periods=offset)


