from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/hello")
def hello():
    with open('file.txt', 'r') as file:
        text = file.read()
    return text

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)