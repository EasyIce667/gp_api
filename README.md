# Gaussian Process Regression API

This project implements a FastAPI-based machine learning service to predict material impact strength from experimental parameters **using Gaussian Process Regression**.

---

## Overview

Scientists run experiments with different material compositions and processing parameters.  
This API learns from historical experiments **(taken parameters available in: data/training_data.json)** and predicts impact strength for new parameter combinations, including uncertainty estimates.

---

## Tech Stack

- FastAPI – REST API framework.
- Scikit-learn – For ML model. **(Gaussian Process Regression)**
- Pydantic – Request validation.
- Joblib – To save Model.
- Pytest – For Testing purposes.

---

## API Endpoints

### 1. View Training Data
**GET** `/api/data`

Returns all available experimental trials and total count from **data/training_data.json**.

---

### 2. Train Model
**POST** `/api/model/train`

- Trains a Gaussian Process Regressor on all available data. **(ml/gp_model.py)**  
- Saves the trained model to local. **(ml/gp_model.joblib)**  
- Returns R² score.

---

### 3. Predict Impact Strength
**POST** `/api/model/predict`

Input:
```json
{
  "epdm_content": 17.5,
  "talc_content": 9.0,
  "processing_temp": 120.0,
  "screw_speed_rpm": 250.0
}
- Result is shown in **results** folder.