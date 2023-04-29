import pandas as pd
import numpy as np

url_types = ["娱乐", "视频", "学习", "社交", "网课", "购物", "游戏"]


def gen_url_types(length):
    return np.random.choice(url_types, length)


dataset = pd.read_csv("./dataset.csv")
dataset = dataset.loc[:, ~dataset.columns.str.contains("^Unnamed")]
all_types = gen_url_types(len(dataset))
dataset["url"] = all_types
dataset["time"] = pd.to_datetime(dataset["time"])

print(dataset)
# dataset.to_csv("dataset2.csv", index=False)
