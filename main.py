from fastapi import FastAPI
import json
from pathlib import Path
from ml.gp_model import train_model, predict_gp
from models import PredictFeatures
from fastapi import HTTPException

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


# 1.view data
@app.get("/api/data")
def view_data():
    data = load_training_data()
    trial_data = data.get("trials",[])

    return{
        "Trials": trial_data,
        "count":len(trial_data)
    }

# 2.train model
@app.post("/api/model/train")
def train_model_endpoint():
    data = load_training_data()
    trial_data = data.get("trials",[])

    if not trial_data:
        return{
            "status":"failed",
            "message": "no training data available"
        }
    score = train_model(trial_data)
    
    return{
        "message":"model trained sucess",
        "total training sample": len(trial_data),
        "R2 Score": score
    }

# 3. predict
@app.post("/api/model/predict")
def predict_model_endpoint(input_data: PredictFeatures):
    try:
        mean, std = predict_gp(input_data.model_dump())
    except RuntimeError:
        raise HTTPException(status_code = 400, detail= "model not trained yet")
    
    return{
        "predict_impact_strength":mean,
        "uncertainity":std
    }


              