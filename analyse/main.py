import pandas as pd


def used_by_hour(data: pd.DataFrame):
    data["timestamp"] = pd.to_datetime(data["time"])
    data["hour"] = data["timestamp"].dt.hour
    result = data.groupby("hour")["account"].nunique()
    return result
