from pymongo import MongoClient
from tinydb import TinyDB, Query
from bson import json_util
import json
import pytz

tzinfo = pytz.timezone("Asia/Shanghai")

CONNECTION_STRING = "mongodb://127.0.0.1:27017/"

db = MongoClient(CONNECTION_STRING, tz_aware=True, tzinfo=tzinfo)["net-behaviour"]


class SessionStore:
    def __init__(self):
        self.db = TinyDB("session.json")

    def __getitem__(self, key):
        info = Query()
        return self.db.search(info.key == key)[0]["value"]

    def __setitem__(self, key, value):
        value = json.loads(json_util.dumps(value))
        self.db.insert({"key": key, "value": value})

    def __contains__(self, key):
        info = Query()
        results = self.db.search(info.key == key)
        return len(results) > 0

    def get(self, key, default):
        if key in self:
            return self[key]
        return default


session_info = SessionStore()
