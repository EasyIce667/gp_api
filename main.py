from fastapi import FastAPI
import json
from pathlib import Path


DATA_PATH = Path("data/training_data.json")

#just to check if fastapi is working 
app = FastAPI()
@app.get("/")
def health():
    return{
        "status": "ok"
    }
#loading json data
def load_training_data():
    if not DATA_PATH.exists():
        return {"trials":[]}
    
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
        return data


#view data
@app.get("/api/data")
def view_data():
    data = load_training_data()
    trial_data = data.get("trials",[])

    return{
        "Trials": trial_data,
        "count":len(trial_data)
    }



              