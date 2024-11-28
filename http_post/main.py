from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Define a Pydantic model for the request body
class Item(BaseModel):
    name: str="stranger"


@app.post("/hello")
def register(item: Item):
    return {"message": f"Hello {item.name}!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)