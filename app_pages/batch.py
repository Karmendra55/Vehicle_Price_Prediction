import streamlit as st
import pandas as pd
import os, time
import plotly.express as px

from src.model_loader import load_model
from sklearn.metrics.pairwise import euclidean_distances

# --- Loading model & dataset ---
MODEL = load_model()
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'dataset.csv')
df = pd.read_csv(dataset_path).dropna(subset=['price']).reset_index(drop=True)

def show():
    """
    Render the Batch Prediction interface for the Vehicle Price Predictor app.

    This function allows users to upload a CSV dataset of vehicles, preview the data,
    run batch predictions using the trained model, and explore insights through
    tables and visualizations. It also provides an option to download the predictions
    as a CSV file.

    Workflow
    --------
    1. Prompt the user to upload a `.csv` file with vehicle data.
    2. Load and preview the dataset.
    3. Run predictions on all rows using the trained `MODEL`:
    4. Display prediction results (top 20 rows).
    5. Generate visual insights:
    6. Provide a download button for saving predictions as a CSV file.

    Notes
    -----
    - Relies on a global trained `MODEL` object with a `.predict()` method.
    - Expected input dataset should include features compatible with the model.
    - Gracefully handles missing or invalid columns for specific plots
    - Adds temporary column `_predicted_price_num` for numeric predictions.

    Returns
    -------
    None
        The function outputs interactive content directly to the Streamlit app.

    """
    st.subheader("📂 Batch Prediction")
    st.markdown("---")

    batch_df = None
    uploaded_file = st.file_uploader("Upload your vehicle dataset (.csv)", type=["csv"])
    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
        st.success(f"✅ File loaded successfully with {batch_df.shape[0]} rows.")

    # --- Preview ---
    if batch_df is not None:
        with st.expander("🔍 Preview Dataset", expanded=True):
            st.dataframe(batch_df.head(10), use_container_width=True)

        # --- Prediction ---
        if st.button("Predict Batch"):
            with st.spinner("Analyzing batch vehicle prices..."):
                time.sleep(4.5)
                # --- N umeric predictions ---
                batch_df["_predicted_price_num"] = MODEL.predict(batch_df).astype(float)

                # --- Formatted for display & CSV ---
                batch_df["Predicted_price"] = batch_df["_predicted_price_num"].map(lambda x: f"{x:.2f}")
            
            # --- Results ---
            st.markdown("### 💰 Prediction Results")
            st.dataframe(batch_df.drop(columns=["_predicted_price_num"]).head(20), use_container_width=True)

            # --- Graphs ---
            st.markdown("### 📊 Batch Insights")

            col1, col2 = st.columns(2)

            with col1:
                fig1 = px.histogram(batch_df, x="_predicted_price_num", nbins=20, title="Distribution of Predicted Prices")
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                if "make" in batch_df.columns:
                    avg_make = batch_df.groupby("make")["_predicted_price_num"].mean().sort_values()
                    fig2 = px.bar(avg_make, title="Average Predicted Price per Make")
                    st.plotly_chart(fig2, use_container_width=True)

            if "year" in batch_df.columns and "mileage" in batch_df.columns:
                scatter_df = batch_df.dropna(subset=["year", "mileage", "_predicted_price_num"]).copy()
                scatter_df = scatter_df[scatter_df["mileage"] > 0]

                if not scatter_df.empty:
                    fig3 = px.scatter(
                        scatter_df,
                        x="year", 
                        y="_predicted_price_num",
                        size="mileage",
                        color="make" if "make" in scatter_df.columns else None,
                        title="Price vs Year (Bubble size = Mileage)"
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                else:
                    st.info("⚠️ Not enough valid data for scatter plot (missing year/mileage).")

            # --- Download Option ---
            csv_bytes = batch_df.drop(columns=["_predicted_price_num"]).to_csv(index=False).encode("utf-8")
            st.download_button(
                "💾 Download Predictions as CSV",
                data=csv_bytes,
                file_name="batch_predictions.csv",
                mime="text/csv",
            )
