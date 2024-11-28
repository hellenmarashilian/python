from fastapi import FastAPI
import os
import uvicorn

app = FastAPI()

@app.get("/hello")
def getenv():
    #set user_name=hell-m
    user = os.getenv("user_name")
    return  "environment variable is: "+ user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)