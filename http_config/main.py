from fastapi import FastAPI
import uvicorn
import configparser

app = FastAPI()

config = configparser.ConfigParser()
config.read('config.ini')

@app.get("/hello")
def hello():
    user_name=config['settings']['user_name']
    return user_name

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)