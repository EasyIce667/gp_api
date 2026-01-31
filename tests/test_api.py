import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

MODEL_PATH = Path("ml/gp_model.joblib")

# test 1. data retrival
def test_get_data():
    response = client.get("/api/data")
    assert response.status_code == 200
    data = response.json()
    assert "Trials" in data
    assert "count" in data
    assert data["count"] >0

# test 2. model training 
def test_train_data():
    response = client.post("/api/model/train")
    assert response.status_code ==200
    data = response.json()
    assert "R2 Score" in data
    assert MODEL_PATH.exists()


# test 3. prediction sucess case
def test_prediction_sucess():
    response = client.post("/api/model/train")
    payload ={
        "epdm_content":17.5,
        "talc_content":9.0,
        "processing_temp":120.0,
        "screw_speed_rpm":250.0
    }
    response = client.post("/api/model/predict",json=payload)
    assert response.status_code ==200
    data = response.json()
    assert "predict_impact_strength" in data
    assert "uncertainity" in data


# test 4. prediction without trained model
def test_prediction_without_training():
    if MODEL_PATH.exists():
        os.remove(MODEL_PATH)

    payload = {
        "epdm_content": 17.5,
        "talc_content": 9.0,
        "processing_temp": 120.0,
        "screw_speed_rpm": 250.0
    }

    response = client.post("/api/model/predict", json=payload)
    assert response.status_code == 400


# test 5. input validation(missing field)
def test_input_validation():
    payload = {
        "epdm_content": 17.5,
        "talc_content": 9.0
    }

    response = client.post("/api/model/predict", json=payload)
    assert response.status_code == 422
