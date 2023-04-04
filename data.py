import pandas as pd


class LazyList:
    def __init__(self, file, encoding):
        self.file = file
        with open(file, encoding=encoding) as f:
            self.length = sum(1 for line in f) - 1

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop = key.start, key.stop
            if start is None:
                start = 0
            if stop is None:
                stop = self.length
            return load_dataset(start, stop - start).to_dict("records")
        elif isinstance(key, int):
            return load_dataset(key, 1).to_dict("records")[0]
        return None

    def __len__(self):
        return self.length


def load_dataset(offset=0, limit=100):
    return pd.read_csv(
        "data/train_data.csv",
        encoding="gbk",
        skiprows=[i for i in range(1, offset + 1)],
        nrows=limit,
    )


def load_dataset_columns():
    return pd.read_csv("data/train_data.csv", encoding="gbk", nrows=0).columns


def load_lazy_list():
    return LazyList("data/train_data.csv", encoding="gbk")
