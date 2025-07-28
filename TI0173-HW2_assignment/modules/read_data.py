import pandas as pd

def read(path:str):
    df = pd.read_csv(path)
    return df
