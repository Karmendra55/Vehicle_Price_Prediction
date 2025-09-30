import pandas as pd
from src.model_loader import load_model
import os

dataset_path = os.path.join(os.path.dirname(__file__), 'dataset', 'dataset.csv')

# --- Read CSV file into DataFrame ---
df = pd.read_csv(dataset_path)

# --- Get unique values for each column ---
unique = {col: df[col].unique() for col in df.columns}

for col, values in unique.items():
    print(f"Column '{col}': {values}")
