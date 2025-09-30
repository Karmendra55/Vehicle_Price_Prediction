import joblib
import streamlit as st
import os

@st.cache_resource
def load_model():
    """
    Load and cache the trained vehicle price prediction model.

    This function loads a pre-trained Model stored as a `.pkl` file and
    caches it using Streamlit's caching mechanism for performance.
    The cached model is reused across app runs until the underlying file changes.

    Returns
    -------
    object
        The trained machine learning model loaded from disk (e.g., a DecisionTreeRegressor).

    """
    path = os.path.join(os.path.dirname(__file__), '..', 'model', 'vehicle_price_dt.pkl')
    return joblib.load(path)