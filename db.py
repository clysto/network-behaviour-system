from pymongo import MongoClient

from config import CONNECTION_STRING

db = MongoClient(CONNECTION_STRING)["net-behaviour"]
