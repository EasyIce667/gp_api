import numpy as np
import joblib
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel
from pathlib import Path



MODEL_PATH = Path("ml/gp_model.joblib")
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

#training model
def train_model(trials):
    X,Y = [],[]

    for trial in trials:
        params= trial["parameters"]
        result = trial["result"]
        
        X.append([
        params["epdm_content"],
        params["talc_content"],
        params["processing_temp"],
        params["screw_speed_rpm"]
        ])
        Y.append(result["impact_strength"])

    X = np.array(X)
    y = np.array(Y)

    #defining kernels 
    kernel = ConstantKernel(1.0) * RBF(length_scale=1.0)

    #creating model 
    model = GaussianProcessRegressor(kernel = kernel, normalize_y = True)

    #train
    model.fit(X,Y)

    #save model 
    joblib.dump(model,MODEL_PATH)

    #scores
    score = model.score(X,y)
    return score

#creating prediction function
def predict_gp(input_feat):
    
    if not MODEL_PATH.exists():
        raise RuntimeError("model not found")
    model = joblib.load(MODEL_PATH)

    X = np.array([[
        input_feat["epdm_content"],
        input_feat["talc_content"],
        input_feat["processing_temp"],
        input_feat["screw_speed_rpm"]
    ]])

    mean, std = model.predict(X,return_std = True)
    return mean[0],std[0]




