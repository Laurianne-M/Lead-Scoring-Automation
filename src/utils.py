import os
import pandas as pd

def file_exists_and_not_empty(filepath: str) -> bool:
    return os.path.isfile(filepath) and os.path.getsize(filepath) > 0

def load_csv_if_exists(filepath: str):
    if not file_exists_and_not_empty(filepath):
        print(f"[INFO] File does NOT exist or is empty: {filepath}")
        return None

    try:
        df = pd.read_csv(filepath)
        print(f"[INFO] Loaded CSV: {filepath}")
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load CSV: {e}")
        return None
    

def load_file(relative_path: str):

    # access 'Data/my_data.csv' relative to the script's location:
    script_dir = os.path.dirname(__file__)
    #full relative path including relative path of csv + current script's location: 
    full_path = os.path.join(script_dir, relative_path) 

    df = load_csv_if_exists(full_path)

    if df is not None:
        print(df.head())
    
    return df

