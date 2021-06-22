import pandas as pd

def ewm(_list):
    df = pd.DataFrame(_list)

    avg = df.ewm(span=len(_list), adjust=False).mean()

    return avg.values.tolist()[-1][0]
