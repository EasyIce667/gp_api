from fastapi import FastAPI
import json

DATA_PATH = "data/traning_data.json"


app = FastAPI()
@app.get("/")
def health():
    return{
        "status": "ok"
    }

def load_traning_data():
    if not DATA_PATH.exists():
        return {"trials":[]}
    
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
        return data
