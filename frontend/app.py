import streamlit as st
import pandas as pd
import requests 

API_BASE_URL = "https://127.0.0.1:8000"

st.set_page_config(
    page_title="Material impact strength Predictor",
    page_icon="🧪",
    layout="wide"
)