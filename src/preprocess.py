import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# --- Define columns ---
NUMERIC_COLS = ["year", "price", "cylinders", "mileage"]
CATEGORICAL_COLS = [
    "make", "model", "fuel", "transmission", "trim", "body", "doors",
    "exterior_color", "interior_color", "drivetrain", "engine"
]
TEXT_COLS = ["name", "description"]

def build_preprocessor():
    """
    Creates preprocessing pipeline for numeric + categorical features.
    
    Returns
    -------
    Preprocessor that will be used in the predictions outcome.
    """
    # --- Numeric: impute missing with median, then scale ---
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    # --- Categorical: input missing with "Unknown", then one-hot encode ---
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    # --- Combine transformations ---
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_COLS),
            ("cat", categorical_transformer, CATEGORICAL_COLS)
        ],
        remainder="drop"
    )

    return preprocessor

def preprocess_input(df: pd.DataFrame):
    """
    Preprocesses vehicle dataset for ML models.
    
    Input
    -----
    Raw DataFrame with vehicle columns.
    
    Returns
    -------
    Preprocessed numpy array (ready for model).
    """
    preprocessor = build_preprocessor()
    processed = preprocessor.fit_transform(df)
    return processed
