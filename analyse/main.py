import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans


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


def k_means(data: pd.DataFrame, cols, k=4):
    train_data = data
    train_data["time"] = pd.to_datetime(train_data["time"])
    train_data["hour"] = train_data["time"].dt.hour
    train_data["weekday"] = train_data["time"].dt.weekday
    train_data["year"] = train_data["time"].dt.year
    train_data["month"] = train_data["time"].dt.month
    train_data["day"] = train_data["time"].dt.day
    train_data_col = train_data.filter([cols])
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(
        scaler.fit_transform(train_data_col), columns=train_data_col.columns
    )
    kmeans = KMeans(n_clusters=k, n_init="auto")
    kmeans.fit(df_scaled)
    train_data_col["cluster"] = kmeans.labels_
    train_data_col["id"] = train_data["id"]
    return train_data_col
