import streamlit as st
import pandas as pd
import requests 

API_BASE_URL = "https://127.0.0.1:8000"

st.set_page_config(
    page_title="Material impact strength Predictor",
    page_icon="🧪",
    layout="wide"
)

# main title 
st.title("🧪 Material Impact Strength Predictor")

# side bar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["View Training data","Train Model (Gaussian Process)","Predict Impact Strength"]

)

# view training data
if page == "View Training data":
    st.header("Training Dataset")

    if st.button("Load Data"):
        responce = requests.get(f"{API_BASE_URL}/api/data")

        if responce.status_code == 200:
            data = responce.json()
            trial_data = data["trials"]

            df = pd.json_normalize(trial_data)
            st.dataframe(df, use_container_width=True)

            st.success(f"Total Samples:{len(trial_data)}")
        else:
            st.error("Failed to Load data")


