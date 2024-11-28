from fastapi import FastAPI
import uvicorn
import configparser
from pymongo import MongoClient


app = FastAPI()


config = configparser.ConfigParser()
config.read('config.ini')


client = MongoClient(config["settings"]["db_connection_string"])
db_accounts = client["accounts"]

#test test
@app.get("/users")
def users_all():
    users_collection = db_accounts["users"]
    db_users = list(users_collection.find())
    returnlist = []
    for user in db_users:
       user["_id"] = str(user["_id"])
       returnlist.append(user)
    return returnlist

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)