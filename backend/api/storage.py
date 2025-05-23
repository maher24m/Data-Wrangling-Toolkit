import os
import pandas as pd
import shutil

# Directories
DATASET_DIRECTORY = "stored_datasets"

# Ensure directories exist
os.makedirs(DATASET_DIRECTORY, exist_ok=True)

def _dataset_path(name: str) -> str:
    return os.path.join(DATASET_DIRECTORY, f"{name}.parquet")

def save_dataset(name: str, data) -> str | None:
    path = _dataset_path(name)
    df = pd.DataFrame(data)
    try:
        df.to_parquet(path, compression="snappy", engine="pyarrow")
        return path
    except Exception as e:
        print(f"[storage] Error saving dataset '{name}': {e}")
        return None

def get_dataset(name: str) -> pd.DataFrame | None:
    path = _dataset_path(name)
    if not os.path.exists(path):
        return None
    try:
        return pd.read_parquet(path, engine="pyarrow")
    except Exception as e:
        print(f"[storage] Error loading dataset '{name}': {e}")
        return None

def list_datasets() -> list[str]:
    files = os.listdir(DATASET_DIRECTORY)
    return [os.path.splitext(f)[0] for f in files if f.lower().endswith(".parquet")]

def delete_dataset(name: str) -> bool:
    path = _dataset_path(name)
    if not os.path.exists(path):
        return False
    try:
        os.remove(path)
        return True
    except Exception as e:
        print(f"[storage] Error deleting dataset '{name}': {e}")
        return False
