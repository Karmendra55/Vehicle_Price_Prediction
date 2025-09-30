import streamlit as st
import pandas as pd
from src.model_loader import load_model
import os, time
import plotly.express as px

from sklearn.metrics.pairwise import euclidean_distances
from src.styles import color_name, get_contrast_color

# --- Model ---
MODEL = load_model()

def reset_if_changed(key, widget_func, *args, **kwargs):
    """Wrapper: resets prediction if the user changes a value"""
    value = widget_func(*args, **kwargs, key=key)
    if "predict_clicked" in st.session_state and st.session_state.predict_clicked:
        if "last_values" not in st.session_state:
            st.session_state.last_values = {}
        old_val = st.session_state.last_values.get(key, None)
        if old_val is not None and old_val != value:
            st.session_state.predict_clicked = False
            st.session_state.predicted_price = None
            st.session_state.input_df = None
    # Save latest value
    if "last_values" not in st.session_state:
        st.session_state.last_values = {}
    st.session_state.last_values[key] = value
    return value

def show():
    """
    Render the main interface of the Vehicle Price Predictor application.

    This function defines the core Streamlit layout and behavior for two modes
    of interaction: **Basic Mode** and **Full Prediction**. It loads the vehicle
    dataset, manages Streamlit session state, and provides interactive tools
    for users to explore vehicles, filter results, or predict prices using a
    trained ML model.

    Workflow
    --------
    1. Load the dataset from `dataset/dataset.csv` and clean missing prices.
    2. Display a segmented control for switching between:
    3. Basic Mode: Explore vehicles by brand, price range, model, and description.
    4. Full Prediction: Enter detailed specifications and predict vehicle price.

    Notes
    -----
    - Session state variables tracked:
        * `input_df` (pd.DataFrame): Last prediction input.
        * `predicted_price` (float): Most recent predicted price.
        * `predict_clicked` (bool): Whether the user requested a prediction.
        * `last_mode` (str): Last active mode.
        * `filtered_df` (pd.DataFrame): Vehicles matching filters in Basic Mode.
        * `selected_car` (str): Persisted selection for chosen car.
    - Relies on external helpers:
        * `color_name(hex)`: Maps hex color to human-readable name.
        * `get_contrast_color(fg, bg)`: Ensures readable text contrast.
        * `MODEL`: Trained ML model for predictions.

    Returns
    -------
    None
        Content is rendered directly to the Streamlit app.
    """
    st.subheader("🚙 Vehicle Input Predictions")
    
    # --- Loading dataset ---
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'dataset.csv')
    df = pd.read_csv(dataset_path)
    df = df.dropna(subset=['price']).reset_index(drop=True)

    # --- Feature Switching Tabs ---
    mode = st.segmented_control(
        "Select Mode",
        ["Basic Mode", "Full Prediction"],
        default="Basic Mode"
    )

    # --- Initialize Session State ---
    if "input_df" not in st.session_state:
        st.session_state.input_df = None
    if "predicted_price" not in st.session_state:
        st.session_state.predicted_price = None
    if "predict_clicked" not in st.session_state:
        st.session_state.predict_clicked = False
    if "last_mode" not in st.session_state:
        st.session_state.last_mode = None
    if st.session_state.last_mode != mode:
        st.session_state.predict_clicked = False
        st.session_state.predicted_price = None
        st.session_state.input_df = None
    st.session_state.last_mode = mode
    
    # -------------------------
    # --- Tab 1: Basic Mode ---
    # -------------------------
    if mode == 'Basic Mode':
        st.subheader("📋 Filter Vehicles by Brand / Price Range")

        # --- Filters ---
        brands = ['All'] + sorted(df['make'].unique().tolist())
        selected_brand = st.selectbox("Select Brand", brands)

        min_price = int(df['price'].min())
        max_price = int(df['price'].max())
        price_range = st.slider(
            "Price Range ($)",
            min_price,
            max_price,
            (min_price, max_price),
            step=1000
        )
        model_name_input = st.text_input("Model Name")
        desc_query = st.text_input("Search in Description (Optional)")

        # --- Search button ---
        if st.button("🔍 Search"):
            filtered_df = df[
                (df['price'] >= price_range[0]) & (df['price'] <= price_range[1])
            ]
            if selected_brand != 'All':
                filtered_df = filtered_df[filtered_df['make'] == selected_brand]
            if model_name_input:
                filtered_df = filtered_df[
                    filtered_df['model'].str.contains(model_name_input, case=False, na=False)
                ]
            if desc_query:
                filtered_df = filtered_df[
                    filtered_df['description'].str.contains(desc_query, case=False, na=False)
                ]
            st.session_state.filtered_df = filtered_df.reset_index(drop=True)

        # --- Display if we already have results ---
        if "filtered_df" in st.session_state:
            filtered_df = st.session_state.filtered_df

            with st.spinner("Crunching numbers..."):
                time.sleep(1.5)
                st.write(f"Showing {len(filtered_df)} vehicles")

                if not filtered_df.empty:
                    display_cols = ['name','make','model','year','price','fuel','body']
                    st.dataframe(filtered_df[display_cols], use_container_width=True)

                    car_names = [
                        f"{row.year} {row.make} {row.model} - ${row.price:,.0f}"
                        for _, row in filtered_df.iterrows()
                    ]

                    if "selected_car" not in st.session_state:
                        st.session_state.selected_car = car_names[0]

                    selected_car = st.selectbox(
                        "Select a car to view details",
                        options=car_names,
                        key="selected_car"
                    )

                    # --- Details for selected car ---
                    car_row = filtered_df.iloc[car_names.index(selected_car)]
                    st.markdown("---")
                    st.markdown(f"### 🚗 {car_row['year']} {car_row['make']} {car_row['model']}")
                    st.write(f"**Price:** ${car_row['price']:,}")
                    st.write(f"**Fuel:** {car_row['fuel']}")
                    st.write(f"**Body:** {car_row['body']}")
                    st.write(f"**Description:** {car_row['description']}")
                else:
                    st.warning("No vehicles found for the selected filters.")

    # ------------------------------
    # --- Tab 2: Full Prediction ---
    # ------------------------------
    elif mode == 'Full Prediction':
        _, col2, _ = st.columns([0.5,5,0.5])
        with col2:
            st.subheader("🔧 Enter Vehicle Specifications")

            # --- Vehicle Input Form ---
            col1, col2 = st.columns([1, 1])
            with col1:
                make = st.selectbox(
                    "Make",
                    sorted(df['make'].dropna().unique()),
                    index=0,
                    help="Select the brand/manufacturer of the vehicle."
                )
            with col2:
                model_name = st.selectbox(
                    "Model",
                    sorted(df['model'].dropna().unique()),
                    index=0,
                    help="Choose the model of the car."
                )

            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            with col1:
                year = st.number_input("Year", int(df['year'].min()), int(df['year'].max()), 2024)
            with col2:
                doors = st.number_input("Doors", 2, 6, 4)
            with col3:
                cylinders = st.number_input("Cylinders", 2, 16, 6)
            with col4:
                mileage = st.number_input("Mileage (mpg)", 0.0, 100.0, 15.0)

            col1, col2 = st.columns([1, 1])
            with col1:
                body = st.selectbox("Body", sorted(df['body'].dropna().unique()), index=0)
                trim = st.text_input("Trim", "Series II")
                engine = st.text_input("Engine", "24V GDI DOHC Twin Turbo")
            with col2:
                transmission = st.selectbox("Transmission", sorted(df['transmission'].dropna().unique()), index=0)
                fuel = st.selectbox("Fuel", ["Gasoline", "Diesel", "Electric", "Hybrid"])
                drivetrain = st.selectbox("Drivetrain", sorted(df['drivetrain'].dropna().unique()), index=0)

            # --- Color pickers ---
            _, col1, col2, col3, col4, _ = st.columns([1,2,1.5,1.5,2,1])
            with col2:    
                exterior_color = st.color_picker("Exterior Color", "#ffffff")
            with col1:    
                st.write(f"**Selected:** {color_name(exterior_color)}")
            with col3:
                interior_color = st.color_picker("Interior Color", "#000000")
            with col4:
                st.write(f"**Selected:** {color_name(interior_color)}")

            # --- Predict button ---
            if st.button("Predict"):
                input_df = pd.DataFrame([{
                    "make": make,
                    "model": model_name,
                    "year": year,
                    "engine": engine,
                    "cylinders": cylinders,
                    "fuel": fuel,
                    "mileage": mileage,
                    "transmission": transmission,
                    "trim": trim,
                    "body": body,
                    "doors": doors,
                    "exterior_color": exterior_color,
                    "interior_color": interior_color,
                    "drivetrain": drivetrain
                }])

                    
                with st.spinner("Analyzing the Price of Car..."):
                    time.sleep(2.5)    
                    price = MODEL.predict(input_df)[0]
                st.session_state.predicted_price = price
                st.session_state.input_df = input_df
                st.session_state.predict_clicked = True
                          

            # --- Prediction Output ---
            if st.session_state.get("predict_clicked", False):
                price = st.session_state.predicted_price
                input_df = st.session_state.input_df 
                text_color = get_contrast_color(interior_color, exterior_color)

                # --- Predicted Price Card ---
                st.markdown(f"""
                <div style="
                    background: linear-gradient(145deg, {interior_color}, {exterior_color});
                    padding: 25px;
                    border-radius: 15px;
                    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
                    text-align:center;
                ">
                    <h2 style="color:{text_color}; font-weight:700;">💰 Predicted Price</h2>
                    <h1 style="font-size:36px; color:{text_color};">${price:,.2f}</h1>
                        <h3 style="color:{text_color};">🚗 Vehicle Details</h3>
                        <ul style="list-style:none; padding-left:2px; font-size:18px; color:{text_color};">
                            <li><b>Maker Brand:</b> {make}</li>
                            <li><b>Model:</b> {model_name}</li>
                            <li><b>Build Year:</b> {year}</li>
                            <li><b>Trim:</b> {trim}</li>
                            <li><b>Engine:</b> {engine}</li>
                            <li><b>Cylinders:</b> {cylinders}</li>
                            <li><b>Fuel Type:</b> {fuel}</li>
                            <li><b>Transmission:</b> {transmission}</li>
                            <li><b>Drivetrain:</b> {drivetrain}</li>
                            <li><b>Body Type:</b> {body}</li>
                            <li><b>No. of Doors:</b> {doors}</li>
                            <li><b>Mileage:</b> {mileage} mpg</li>
                            <li><b>Exterior Color:</b> {color_name(exterior_color)}</li>
                            <li><b>Interior Color:</b> {color_name(interior_color)}</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                # --- Similar Vehicles ---
                st.markdown("### 🚘 Similar Vehicles")
                features = ["year", "mileage", "cylinders", "doors"]

                df_numeric = df[features].fillna(0)
                input_df_filled = input_df[features].fillna(0)

                distances = euclidean_distances(df_numeric, input_df_filled)
                closest_idx = distances.argmin()
                similar_car = df.iloc[closest_idx]

                st.write(f"Closest Vehicle: **{similar_car['year']} {similar_car['make']} {similar_car['model']} - ${similar_car['price']:,}**")

                # --- Feature Comparison ---
                st.markdown("### 📊 Feature Comparison")
                comp_df = pd.DataFrame({
                    "Feature": features,
                    "Your Car": [year, mileage, cylinders, doors],
                    "Closest Car": [similar_car[f] for f in features]
                })
                fig = px.bar(comp_df, x="Feature", y=["Your Car", "Closest Car"], barmode="group", text_auto=True)
                st.plotly_chart(fig, use_container_width=True)
