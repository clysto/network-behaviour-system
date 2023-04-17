from pymongo import MongoClient

CONNECTION_STRING = "mongodb://127.0.0.1:27017/"

db = MongoClient(CONNECTION_STRING)["net-behaviour"]

session_info = {}
