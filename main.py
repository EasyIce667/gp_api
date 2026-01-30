from fastapi import FastAPI
import json

Data_path = "data/traning_data.json"


app = FastAPI()
@app.get("/")
def health():
    return{
        "status": "ok"
    }