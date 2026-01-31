import numpy as np
import joblib
from sklearn.gaussian_process import GaussianPocessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel
from pathlib import Path


X,Y = [],[]
def train_model(trials):

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
Y = np.array(Y)

#defining kernels 
kernel = ConstantKernel(1.0) * RBF(length_scale=1.0)
