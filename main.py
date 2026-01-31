from fastapi import FastAPI
import json
from pathlib import Path
from ml.gp_model import train_model, predict_gp
from models import PredictFeatures
from fastapi import HTTPException



#just to check if fastapi is working 
app = FastAPI()
@app.get("/")
def health():
    return{
        "status": "ok"
    }

DATA_PATH = Path("data/training_data.json")
#loading json data
def load_training_data():
    if not DATA_PATH.exists():
        return {"trials":[]}
    
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
        return data

def get_training_ranges(trials):
    ranges= {
        "epdm_content":[],
        "talc_content":[],
        "processing_temp":[],
        "screw_speed_rpm":[]
    }
    for trial in trials:
        params = trial["parameters"]
        for key in ranges:
            ranges[key].append(params[key])

    return{
        key:(min(values),max(values))
        for key, values in ranges.items()
    }


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
    input_dict = input_data.model_dump()
    try:
        mean, std = predict_gp(input_dict)
    except RuntimeError:
        raise HTTPException(status_code = 400, detail= "model not trained yet")
    
    # range warnings
    data = load_training_data()
    trial_data = data.get("trials",[])
    ranges = get_training_ranges(trial_data)

    warnings = []

    for key, value in input_dict.items():
        min_val, max_val = ranges[key]
        if value < min_val or value > max_val:
            warnings.append(f"{key}={value} is outside training range ({min_val} - {max_val})")
    
    response = {
        "predict_impact_strength":mean,
        "uncertainity":std
    }
    if warnings:
        response["warnings"] = warnings
    
    return response

#extra
#view trial id details
@app.get("/api/data/view/{trial_id}")
def view_trial_id_content(trial_id: int):
    data = load_training_data()
    trial_data = data.get("trials",[])

    for trial in trial_data:
        if trial.get("trial_id") == trial_id:
            return{
                "trial_id":trial_id,
                "trial_data":trial
            }
    raise HTTPException(
        status_code=404,
        detail=f"trial with id {trial_id} not found."
    )


