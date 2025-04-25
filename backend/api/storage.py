import os
import pandas as pd

# Directory where all datasets are stored
DATASET_DIRECTORY = "stored_datasets"
os.makedirs(DATASET_DIRECTORY, exist_ok=True)

def _dataset_path(name: str) -> str:
    """
    Compute the full path for a given dataset name (Parquet).
    """
    return os.path.join(DATASET_DIRECTORY, f"{name}.parquet")

def save_dataset(name: str, data) -> str | None:
    """
    Save a dataset to disk in Parquet format with Snappy compression.
    Overwrites any existing file of the same name.
    Returns the file path on success, or None on error.
    """
    path = _dataset_path(name)
    df = pd.DataFrame(data)
    try:
        df.to_parquet(path, compression="snappy", engine="pyarrow")
        return path
    except Exception as e:
        print(f"[storage] Error saving dataset '{name}': {e}")
        return None

def get_dataset(name: str) -> pd.DataFrame | None:
    """
    Load a dataset from its Parquet file.
    Returns a DataFrame if the file exists and loads successfully, else None.
    """
    path = _dataset_path(name)
    if not os.path.exists(path):
        # No such dataset
        return None
    try:
        return pd.read_parquet(path, engine="pyarrow")
    except Exception as e:
        print(f"[storage] Error loading dataset '{name}': {e}")
        return None

def list_datasets() -> list[str]:
    """
    List all datasets currently stored (by name, without extension).
    """
    files = os.listdir(DATASET_DIRECTORY)
    # Only .parquet files
    return [os.path.splitext(f)[0]
            for f in files
            if f.lower().endswith(".parquet")]

def delete_dataset(name: str) -> bool:
    """
    Delete the Parquet file for the given dataset name.
    Returns True if deleted, False if not found or on error.
    """
    path = _dataset_path(name)
    if not os.path.exists(path):
        return False

    try:
        os.remove(path)
        return True
    except Exception as e:
        print(f"[storage] Error deleting dataset '{name}': {e}")
        return False
