import pandas as pd


def load_dataset(offset=0, limit=100):
    if limit == -1:
        return pd.read_csv(
            "data/train_data.csv",
            encoding="gbk",
            skiprows=[i for i in range(1, offset + 1)],
        )
    else:
        return pd.read_csv(
            "data/train_data.csv",
            encoding="gbk",
            skiprows=[i for i in range(1, offset + 1)],
            nrows=limit,
        )
