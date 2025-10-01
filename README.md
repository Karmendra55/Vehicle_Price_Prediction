# Vehicle Price Prediction

A **Streamlit-based application** for predicting vehicle prices based on specifications, comparing multiple configurations, and exploring structured dataset entries. Powered by **XGBoost**, it delivers a clean, interactive, and functional tool for vehicle price estimation and comparison.

## Dataset Layout

The Dataset and Models are already in place, If you want to change the files you can replace these:

``` markdown
> dataset/
>    dataset.csv

> model/
>    metadata.json
>    vehicle_price_dt.pkl
>    vehicle_price_pipeline.pkl
```

The folder has all the file that we need in the required format, Make sure not to delete any files.

## Quickstart

1) Create and activate a virtual environment
```bash
python -m venv .venv
```
For Linux or Max:
```bash
source .venv/bin/activate
```
For Windows:
```bash
.venv\Scripts\activate
```

2) Now Run the file to install the dependencies
```bash
install_modules.bat
```

Run the Application
3a) Option A
```bash
run.bat
```

3b) Option B
- Open the command/bash and do the follow:
```bash
cd {"Drive:/file/.../Vehicle_Price_Prediction/"}
```
and type
```bash
streamlit run main.py
```

Make sure all files are placed as shown in the dataset layout, Once started, the application will open in your default web browser.

## Objective

- Predict vehicle prices based on user-defined specifications.
- Compare multiple predicted vehicle entries (dataset-based and custom).
- Format and display raw vehicle specs in a user-friendly format.
- Maintain batch predictions and downloading of the results.

## Model

- Algorithm: XGBoost(Before Decision Tree based on `RMSE`) trained on a structured vehicle dataset.
- Features: Brand, model, fuel type, mileage, engine power, and other specifications.
- Output: Predicted vehicle price with comparison options.

## Highlights

> Interactive and clean UI using Streamlit.
> Modular design with separation of logic, UI, and helpers.
> Option to check Insights of the trained dataset and model.
> Supports running via .bat for quick local execution.

## Key Features
- Vehicle Price Predictor → Input vehicle specifications to predict price.
- Multiple Prediction Modes → Basic, Advanced, and Batch prediction options.
- Comparison Tool → Side-by-side comparison of dataset vehicles and user-customized vehicles.
- Dataset Browser → Explore dataset entries for validation and analysis.
- Specification Formatter → Convert raw data into a clean, human-readable specification sheet.

