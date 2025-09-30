import streamlit as st
import datetime

# --- Cached Static Content ---
@st.cache_data
def _get_app_info():
    """
    Retrieve static application information for the Vehicle Price Predictor Dashboard.

    This function returns a dictionary containing the app's metadata, introduction,
    objectives, rules, FAQs, and other descriptive content.

    Returns
    -------
    dict
        A dictionary with the following keys:
        - "title" (str): Application title.
        - "intro" (str): Welcome message and feature overview.
        - "objective" (str): High-level objective of the application.
        - "sample_rules" (list[str]): Key rules and highlights of the prediction model.
        - "faq" (dict): Frequently asked questions with answers, covering:
    """
    return {
        "title": "🚗 Vehicle Price Predictor Dashboard",
        "intro": """
            Welcome to the **Vehicle Price Predictor Application**!  

            This interactive platform helps you:
            - **Find Prices** for vehicles  
            - **Predict prices from specifications**  
            - **Analyze batches of vehicles**  
            - **Explore datasets & insights**
        """,
        "objective": """
            ### 🎯 Objective
            To build an **AI-powered vehicle price prediction system** that estimates vehicle prices
            based on specifications and features.
        """,
        "sample_rules": [
            "💰 Prices are predicted using a trained Decision Tree model.",
            "🏎 Model considers engine, cylinders, fuel, transmission, trim, and more.",
            "📊 Supports Single & Batch predictions.",
            "🧩 Feature importance and dataset insights included."
        ],
        "faq": {
            "📘 What is this app?": """
                The **Vehicle Price Predictor Dashboard** estimates prices for vehicles
                based on features like make, model, year, engine, mileage, and drivetrain.
            """,
            "🤖 How does it predict?": """
                The XGBoost model evaluates the specifications you provide
                and outputs an estimated price.
            """,
            "🧠 Model Details": """
                - **Algorithm**: Decision Tree Regressor  
                - **Training Data**: Vehicle dataset with features and prices  
                - **Preprocessing**: Imputation + One-Hot Encoding + Scaling  
                - **Evaluation Metric**: RMSE, R²
            """,
            "📄 Outputs & Features": """
                - Single vehicle price prediction  
                - Batch price prediction from CSV uploads  
                - Dataset exploration and insights  
            """,
            "📬 Feedback & Credits": """
                - Developed by **Karmendra Bahadur Srivastava**  
                - Dataset by **Unified Mentor**  
                - Having Issues? Email: **[Click Here](mailto:karmendra5902@gmail.com)**  
            """,
        },
    }


def show():
    """
    Render the main dashboard layout for the Vehicle Price Predictor Application.

    This function constructs the Streamlit-based UI, including sidebar navigation,
    greeting messages, introductory text, objectives, usage rules, feature navigation,
    FAQs. 

    Workflow
    --------
    1. Display a sidebar greeting and navigation message.
    2. Show a time-based greeting (morning, afternoon, evening).
    3. Render the introduction, objectives, and sample rules.
    4. Display FAQ and About section with expandable panels.

    Returns
    -------
    None
        The function outputs content directly to the Streamlit app.
    """
    info = _get_app_info()

    # --- Intro ---
    st.markdown(info["intro"])
    st.markdown("---")

    # --- Objective + Sample Rules ---
    st.markdown(info["objective"])
    st.markdown("#### 🚦 How It Works:")
    for rule in info["sample_rules"]:
        st.markdown(f"- {rule}")

    # --- Feature Navigation ---
    st.markdown("---")
    st.subheader("📌 Explore Features")
    st.markdown("""
        - **Single Prediction**: Predict price for one vehicle based on specifications.  
        - **Batch Prediction**: Upload a dataset and predict prices in bulk.  
        - **Extended Insights**: Explore dataset statistics, feature importance, and trends.
    """)

    # --- FAQ / About Section ---
    st.markdown("---")
    st.subheader("ℹ️ About This App")
    for title, content in info["faq"].items():
        with st.expander(title, expanded=False):
            st.markdown(content)

    # --- Footer ---
    st.markdown("---")
    st.caption("💡 Tip: Use the sidebar or buttons above to explore all available tools and datasets.")
