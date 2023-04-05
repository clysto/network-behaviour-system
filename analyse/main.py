import pandas as pd
import numpy as np


def used_by_hour(data: pd.DataFrame):
    data["timestamp"] = pd.to_datetime(data["time"])
    data["hour"] = data["timestamp"].dt.hour
    result = data.groupby("hour")["account"].nunique()
    r = np.zeros(24)
    r[result.index] = result.to_numpy()
    return r.tolist()


def used_by_group(data: pd.DataFrame):
    usage_by_group = data.groupby(["group"])["account"].nunique()
    return usage_by_group
