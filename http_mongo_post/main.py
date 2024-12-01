from fastapi import FastAPI, HTTPException, Request
import uvicorn
import configparser
from pymongo import MongoClient
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

config = configparser.ConfigParser()
config.read('config.ini')

client = MongoClient(config["settings"]["db_connection_string"])
db_accounts = client["accounts"]

class UserModel(BaseModel):
    user_id: int
    name: str
    
class UserIDModel(BaseModel):
    user_id: int

@app.get("/selectall")
def users_all():
    users_collection = db_accounts["users"]
    db_users = list(users_collection.find())
    returnlist = []
    for user in db_users:
       user["_id"] = str(user["_id"])
       returnlist.append(user)
    if not returnlist:
        raise HTTPException(status_code=404, detail="No entries found.")
    return returnlist

#below returns only specified entry from the database
@app.get("/selectbyid")
def select_by_id(UserID: Optional[int] = None):
    if UserID is None:
        raise HTTPException(status_code=400, detail="UserID query parameter is required")
    users_collection = db_accounts["users"]
    user = users_collection.find_one({"user_id": UserID})
    if not user:
        raise HTTPException(status_code=404, detail="Entry not found")
    user["_id"] = str(user["_id"])
    return user

@app.post("/adduser")
def add_user(user: UserModel):
    users_collection = db_accounts["users"]
    existing_user = users_collection.find_one({"user_id": user.user_id})
    if existing_user:
        updated_user = users_collection.update_one({"user_id": user.user_id},{"$set": {"name": user.name}})
        if updated_user.modified_count > 0:
            return {"message": f"User with ID {user.user_id} already exists, and has been updated successfully."}
        else:
            return {"message": f"User with ID {user.user_id} already exists, no changes were made."}
    else:
        new_user = {"user_id": user.user_id, "name": user.name}
        result = users_collection.insert_one(new_user)
        if result.inserted_id:
            return {"message": f"A new user with ID {user.user_id} and name {user.name} has been added successfully"}


@app.post("/deluser")
def delete_user(user: UserIDModel):
    users_collection = db_accounts["users"]
    UserID = user.user_id
    existing_user = users_collection.find_one({"user_id":UserID})
    if not existing_user:
        raise HTTPException(status_code=400, detail=f"No user with ID {UserID} was found")
    result = users_collection.delete_one({ "user_id": UserID })
    if result.acknowledged == True:
        return {"message": f"The user with ID {UserID} and name {existing_user["name"]} has been deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)