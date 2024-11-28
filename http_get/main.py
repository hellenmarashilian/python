from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def hello(name='stranger'):
        #http://127.0.0.1:8000/?name=sadas 
        return {"message" : f'Hello {name}!'}

# Main method checker to run the app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
#uvicorn main:app --reload