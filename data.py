import pandas as pd
from db import db

CACHE = None


def load_dataset(offset=0, limit=100):
    global CACHE
    if limit == -1:
        if CACHE is None:
            records = db["dataset"].find()
            df = pd.DataFrame(list(records))
            CACHE = df
        return CACHE
    else:
        records = db["dataset"].find().skip(offset).limit(limit)
        df = pd.DataFrame(list(records))
        return df
