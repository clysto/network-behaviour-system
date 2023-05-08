import pandas as pd
from db import db

CACHE = None


def load_dataset(offset=0, limit=100, group=None):
    if group is not None:
        filter = {"group": group}
    else:
        filter = {}
    global CACHE
    if limit == -1 and group is None:
        if CACHE is None:
            records = db["dataset"].find(filter)
            df = pd.DataFrame(list(records))
            CACHE = df
        return CACHE
    else:
        records = db["dataset"].find(filter=filter, skip=offset, limit=limit)
        df = pd.DataFrame(list(records))
        return df
