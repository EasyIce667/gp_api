import streamlit as st
import pandas as pd
import requests 

API_BASE_URL = "http://127.0.0.1:8000"

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
    st.header("📊 Training Dataset")

    if st.button("Load Data"):
        response = requests.get(f"{API_BASE_URL}/api/data")

        if response.status_code == 200:
            data = response.json()
            trial_data = data["Trials"]

            df = pd.json_normalize(trial_data)
            st.dataframe(df, use_container_width=True)

            st.success(f"Total Samples: {len(trial_data)}")
        else:
            st.error("Failed to Load data")


# training model page
elif page == "Train Model (Gaussian Process)":
    st.header("⚙️ Train Gaussian Process Model")

    st.info("This will train the model using all the available data.")
    if st.button("Train Model"):
        with st.spinner("Training model..."):
            response = requests.post(f"{API_BASE_URL}/api/model/train")
        if response.status_code == 200:
            result = response.json()
            st.success("Model trained sucessfully")
            st.metric("R2 Score", round(result.get("R2 Score",0), 4))
        else:
            st.error("Training Failed")

# prediction page
elif page == "Predict Impact Strength":
    st.header("🔮 Predict Impact Strength")

    col1, col2 = st.columns(2)

    with col1:
        epdm = st.number_input(
            "EPDM Content (%)",min_value=0.0,value=17.5,step=0.1)
        
        talc = st.number_input(
            "Talc Content (%)",min_value=0.0,value=9.0,step=0.1)

    with col2:
        temp = st.number_input(
            "Processing Temperature (°C)",min_value=0.0,value=120.0,step=1.0
        )
        
        rpm = st.number_input(
            "Screw Speed (RPM)",min_value=0.0,value=250.0,step=5.0
        )

    payload = {
        "epdm_content": epdm,
        "talc_content": talc,
        "processing_temp": temp,
        "screw_speed_rpm": rpm
    }

    with st.expander("🔍 Input Summary"):
        st.json(payload)

    if st.button("Predict"):
        with st.spinner("Predicting..."):
            response = requests.post(
                f"{API_BASE_URL}/api/model/predict",
                json=payload
            )

        if response.status_code == 200:
            result = response.json()

            st.success("Prediction successful 🎯")

            col1, col2 = st.columns(2)
            
            col1.metric(
                "Impact Strength",
                f"{result['predict_impact_strength']:.2f}"
            )
            col2.metric(
                "Uncertainty (σ)",
                f"{result['uncertainity']:.2f}"
            )
        else:
            st.error(
                response.json().get("detail", "Prediction failed")
            )