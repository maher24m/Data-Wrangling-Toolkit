import os
import pandas as pd

# 🔥 Define a directory for storing datasets
DATASET_DIRECTORY = "stored_datasets"
DATASET_STORAGE = {}  # 🔥 Dictionary to store dataset references

# 🔥 Ensure the directory exists
if not os.path.exists(DATASET_DIRECTORY):
    os.makedirs(DATASET_DIRECTORY)

def save_dataset(name, data):
    """Save dataset efficiently using Parquet (faster than CSV)."""
    file_path = os.path.join(DATASET_DIRECTORY, f"{name}.parquet")  # 🔥 Unique file for each dataset
    df = pd.DataFrame(data)

    try:
        df.to_parquet(file_path, compression="snappy")  # 🔥 Use Snappy compression for speed
        DATASET_STORAGE[name] = file_path  # 🔥 Store reference to file
        return file_path
    except Exception as e:
        print(f"Error saving dataset: {e}")
        return None

def get_dataset(name):
    """Load a dataset from Parquet file."""
    file_path = DATASET_STORAGE.get(name)
    if not file_path or not os.path.exists(file_path):
        return None  # 🔥 Dataset not found

    try:
        return pd.read_parquet(file_path, engine="pyarrow")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def list_datasets():
    """Return a list of available datasets"""
    return list(DATASET_STORAGE.keys())  # 🔥 Return all dataset names
