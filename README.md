# Vehicle Price Prediction

The Vehicle Price Prediction is a Streamlit-based application that enables users to predict the price based on its specifications, compare multiple configurations, and analyze structured dataset entries. It integrates XGBoost with interactive UI components to provide an intuitive and functional tool for vehicle price estimation and comparison.

## Objective

- Predict vehicle prices based on user-defined specifications.
- Compare multiple predicted vehicle entries (dataset-based and custom).
- Format and display raw vehicle specs in a user-friendly format.
- Maintain batch predictions and downloading of the results.

## Dataset

- The Original Dataset can be found in the root folder `dataset/dataset.csv`

## Installation of the Program

> Firstly Run the `install_modules.bat` file
to download all the dependencies and follow the steps

1. python -m venv
   - venv source > .venv/bin/activate
   - #Windows > .venv\Scripts\active
  
2. Make sure to check wheather all the files are present or not

3. If the install_modules.bat is not working, use command `prompt/Powershell` and type `pip install -r requirement.txt`

## Running the Program

> Click on the `run.bat` to open the program
OR
> Open a terminal and target it towards the root folder `cd {location}`
> Then type `streamlit run main.py`

## Highlights

> Interactive and clean UI using Streamlit.
> Modular design with separation of logic, UI, and helpers.
> Option to check Insights of the trained dataset and model.
> Supports running via .bat for quick local execution.

## Key Features
1. Vehicle Price Predictor: Accepts inputs like brand, model, fuel type, mileage, engine power, and more to predict price using a trained ML model.
2. Multiple Prediction Options: The User can pick Basic, Advanced and Batch Prediction Modes.
3. Comparison Tool: Allows side-by-side price comparison between dataset vehicles and user-customized vehicles.
4. Dataset Browser: Explore structured dataset entries for reference and validation.
5. Specification Formatter: Converts raw data into a clean, human-readable vehicle specification sheet.

