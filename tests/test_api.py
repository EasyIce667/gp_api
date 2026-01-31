import os
from main import app
from fastapi.testclient import TestClient
from pathlib import Path

client = TestClient(app)

MODEL_PATH = Path("ml/gp_model.joblib")
