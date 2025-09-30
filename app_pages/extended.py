import streamlit as st
import pandas as pd
import os
from datetime import datetime
from sklearn.metrics.pairwise import euclidean_distances

from src.model_loader import load_model
from src.styles import card_style

# --- Load model and dataset ---
MODEL = load_model()
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'dataset.csv')
model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'vehicle_price_dt.pkl')
df = pd.read_csv(dataset_path).dropna(subset=['price']).reset_index(drop=True)

def show(df=df, model=MODEL, input_df=None):
    """
    Render the Extended Insights & Analytics section of the Vehicle Price Predictor app.

    This function provides a multi-tab analytics dashboard with three main modes:
    - **Statistics**: Displays feature importance, price trends, similar vehicles, and dataset statistics.
    - **Dataset**: Allows browsing, filtering, searching, and downloading parts of the dataset.
    - **Feature Engineering**: Shows dataset metadata, model details, engineered features, and various charts for deeper analysis.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset containing vehicle information and prices.
    model : object
        The trained machine learning model used for predictions. Should have attributes like
        `feature_importances_`, `n_features_in_`, etc., if applicable.
    input_df : pd.DataFrame, optional
        The most recent vehicle specification used for prediction. Used to display similar vehicles.

    Workflow
    --------
    1. Display a segmented control for navigation between "Statistics", "Dataset", and "Featured Engineering".
    2. **Statistics** mode
    3. **Dataset** mode
    4. **Featured Engineering** mode

    Returns
    -------
    None
        Renders interactive content directly to the Streamlit app.
    """
    card_style()
    st.subheader("📊 Insights & Analytics")
    
    # --- Switching Tabs ---
    mode = st.segmented_control(
        "Navigation",
        ["Statistics", "Dataset", "Featured Engineering"],
        default="Statistics"
    )

    # -------------------------
    # --- Tab 1. Statistics ---
    # -------------------------
    if mode == "Statistics":
        if hasattr(model, "feature_importances_"):
            st.markdown('<div class="card"><h3>🔑 Feature Importance</h3>', unsafe_allow_html=True)
            importance_df = pd.DataFrame({
                "Feature": df.columns.drop("price"),
                "Importance": model.feature_importances_
            }).sort_values(by="Importance", ascending=False)
            st.bar_chart(importance_df.set_index("Feature"))
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>📈 Price Trends</h3>', unsafe_allow_html=True)
        trend_feature = st.selectbox(
            "Select feature for price trend",
            ["make", "year", "body", "fuel", "drivetrain"]
        )
        trend_data = df.groupby(trend_feature)["price"].mean().sort_values()
        st.bar_chart(trend_data)
        st.markdown("</div>", unsafe_allow_html=True)

        if input_df is not None:
            st.markdown('<div class="card"><h3>🚗 Similar Vehicles</h3>', unsafe_allow_html=True)
            features = ["year", "mileage", "cylinders", "doors"]
            distances = euclidean_distances(df[features], input_df[features])
            closest_idx = distances.argmin()
            similar_car = df.iloc[closest_idx]
            st.markdown(f"Closest Vehicle: **{similar_car['year']} {similar_car['make']} {similar_car['model']} - ${similar_car['price']:,}**")
            st.dataframe(similar_car)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>📊 Dataset Statistics</h3>', unsafe_allow_html=True)
        st.write(df["price"].describe())
        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # --- Tab 2. Dataset Viewer ---
    # -----------------------------
    elif mode == "Dataset":
        st.markdown('<div class="card"><h3>👀 Browse Dataset</h3>', unsafe_allow_html=True)

        max_rows = df.shape[0]
        col1, col2 = st.columns(2)
        with col1:
            start_idx = st.number_input("Start row", 0, max_rows - 1, 0)
        with col2:
            end_idx = st.number_input("End row", start_idx + 1, max_rows, min(start_idx + 50, max_rows))

        search_term = st.text_input("🔍 Search (case-insensitive)")
        preview_df = df.iloc[start_idx:end_idx]
        if search_term.strip():
            mask = df.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)
            preview_df = df[mask].iloc[start_idx:end_idx]

        selected_cols = st.multiselect("Columns to display", df.columns.tolist(), default=df.columns.tolist()[:10])
        st.dataframe(preview_df[selected_cols], use_container_width=True)

        csv_bytes = preview_df[selected_cols].to_csv(index=False).encode("utf-8")
        with st.expander("Download the Dataset"):
            st.download_button("💾 Download preview as CSV", data=csv_bytes, file_name="vehicle_data_preview.csv", mime="text/csv")

        st.markdown("</div>", unsafe_allow_html=True)
        
    # ------------------------------
    # --- 3. Feature Engineering ---
    # ------------------------------
    elif mode == "Featured Engineering":

        # --- Dataset Info ---
        st.markdown('<div class="card"><div class="title">📂 Dataset Info</div>', unsafe_allow_html=True)
        dataset_size = os.path.getsize(dataset_path) / 1024  # KB
        last_updated = datetime.fromtimestamp(os.path.getmtime(dataset_path)).strftime("%b %d, %Y")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", f"{df.shape[0]:,}")
        c2.metric("Columns", f"{df.shape[1]}")
        c3.metric("Size", f"{dataset_size:.2f} KB")
        c4.metric("Last Updated", last_updated)

        with st.expander("📑 Columns & Data Types"):
            dtype_df = pd.DataFrame({
                "Column": df.columns,
                "Dtype": df.dtypes.astype(str),
                "Non-Null Count": df.notnull().sum().values
            })
            st.dataframe(dtype_df, use_container_width=True, height=320)
        st.markdown("</div>", unsafe_allow_html=True)

        # --- Model Info ---
        st.markdown('<div class="card"><div class="title">🤖 Model Info</div>', unsafe_allow_html=True)
        if os.path.exists(model_path):
            model_size = os.path.getsize(model_path) / 1024
            last_updated_model = datetime.fromtimestamp(os.path.getmtime(model_path)).strftime("%b %d, %Y")

            c1, c2 = st.columns(2)
            c1.metric("Model Size", f"{model_size:.2f} KB")
            c2.metric("Last Updated", last_updated_model)
        else:
            st.warning("⚠ Model file not found at expected path.")

        if hasattr(model, "n_features_in_"):
            st.write(f"**Features Used:** {model.n_features_in_}")
        if hasattr(model, "classes_"):
            st.write(f"**Target Classes:** {len(model.classes_)}")
        st.markdown("</div>", unsafe_allow_html=True)

        # --- Engineered Features ---
        st.markdown('<div class="card"><div class="title">🧮 Engineered Features</div>', unsafe_allow_html=True)
        df["price_per_mile"] = df["price"] / (df["mileage"].replace(0, 1))
        df["age"] = pd.Timestamp.now().year - df["year"]
        df["luxury_flag"] = df["make"].isin(["BMW", "Mercedes-Benz", "Audi", "Lexus"]).astype(int)

        with st.expander("Preview Engineered Features"):
            st.dataframe(
                df[["make", "model", "year", "mileage", "price", "price_per_mile", "age", "luxury_flag"]].head(10),
                use_container_width=True
            )
        st.markdown("</div>", unsafe_allow_html=True)


        # --- Charts ---
        st.markdown('<div class="card"><div class="title">📊 Charts</div>', unsafe_allow_html=True)

        with st.expander("📉 Average Price by Age"):
            avg_price_by_age = df.groupby("age")["price"].mean().reset_index()
            st.line_chart(avg_price_by_age.set_index("age"))

        with st.expander("💎 Luxury vs Non-Luxury Vehicles"):
            avg_price_luxury = df.groupby("luxury_flag")["price"].mean().rename({0: "Non-Luxury", 1: "Luxury"})
            st.bar_chart(avg_price_luxury)

        with st.expander("🚗 Price per Mile Distribution"):
            st.histogram_chart(df["price_per_mile"], bins=30) if hasattr(st, "histogram_chart") else st.bar_chart(
                df["price_per_mile"].value_counts(bins=30).sort_index()
            )

        with st.expander("⛽ Mileage vs Price"):
            scatter_df = df[["mileage", "price"]].dropna()
            st.scatter_chart(scatter_df, x="mileage", y="price")

        with st.expander("🏷️ Vehicle Distribution by Make (Top 10)"):
            top_makes = df["make"].value_counts().head(10)
            st.bar_chart(top_makes)

        st.markdown("</div>", unsafe_allow_html=True)