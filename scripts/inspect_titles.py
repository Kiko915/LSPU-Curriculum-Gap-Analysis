import pandas as pd
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_csv = os.path.join(base_dir, "data", "raw", "job_dataset.csv")

try:
    df = pd.read_csv(input_csv)
    print("Columns:", df.columns)
    if 'Title' in df.columns:
        print("\nUnique Titles:")
        print(df['Title'].unique())
        print("\nTotal Unique Titles:", df['Title'].nunique())
    elif 'Role' in df.columns:
        print("\nUnique Roles:")
        print(df['Role'].unique())
except Exception as e:
    print(f"Error: {e}")
