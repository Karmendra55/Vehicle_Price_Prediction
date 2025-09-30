import streamlit as st
import datetime

st.set_page_config(
    page_title="Vehicle Price Prediction",
    page_icon="🚗",
    layout=st.session_state.get("layout", "wide"),
    initial_sidebar_state="auto"
)
from app_pages import home, single, extended, batch

st.title("🚗 Vehicle Price Predictor")
st.caption("""This Application is made for the prediction of User Inputted Specifications of a Vehicle, The Model was trained 
           to make it possible for various input types and different outcomes based on them.""")
st.markdown('---')

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Home", "Vehicle Price Prediction", "Batch Prediction", "Insights and Analytics"])

    st.markdown("---")
    # --- Header ---
    now = datetime.datetime.now()
    hour = datetime.datetime.now().hour
    if hour < 12:
        greeting = "☀️ Good Morning!"
    elif hour < 18:
        greeting = "🌤️ Good Afternoon!"
    else:
        greeting = "🌙 Good Evening!"
    current_date = now.strftime("%d %B %Y")  
    st.text(f"{greeting} — Today is {current_date}")

# --- Load Pages ---
if page == "Home":
    home.show()
elif page == "Vehicle Price Prediction":
    single.show()
elif page == "Insights and Analytics":
    extended.show()
elif page == "Batch Prediction":
    batch.show()

# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: grey; font-size:16px;'>"
    " Made with ❤️ | Developed by <b>Karmendra Srivastava</b>  "
    "</p>",
    unsafe_allow_html=True
)