import os
import pandas as pd
import shutil

# Directories
DATASET_DIRECTORY = "stored_datasets"
ACTIVE_DIRECTORY = "active_dataset"

# Ensure directories exist
os.makedirs(DATASET_DIRECTORY, exist_ok=True)
os.makedirs(ACTIVE_DIRECTORY, exist_ok=True)

def _dataset_path(name: str) -> str:
    return os.path.join(DATASET_DIRECTORY, f"{name}.parquet")

def _active_path() -> str:
    return os.path.join(ACTIVE_DIRECTORY, "active.parquet")

def save_dataset(name: str, data) -> str | None:
    path = _dataset_path(name)
    df = pd.DataFrame(data)
    try:
        df.to_parquet(path, compression="snappy", engine="pyarrow")
        return path
    except Exception as e:
        print(f"[storage] Error saving dataset '{name}': {e}")
        return None

def save_active_dataset(data) -> str | None:
    """
    Save a dataset as the active dataset.
    Overwrites any existing active dataset.
    """
    path = _active_path()
    df = pd.DataFrame(data)
    try:
        df.to_parquet(path, compression="snappy", engine="pyarrow")
        return path
    except Exception as e:
        print(f"[storage] Error saving active dataset: {e}")
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

def get_active_dataset() -> pd.DataFrame | None:
    path = _active_path()
    if not os.path.exists(path):
        return None
    try:
        return pd.read_parquet(path, engine="pyarrow")
    except Exception as e:
        print(f"[storage] Error loading active dataset: {e}")
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

def delete_active_dataset() -> bool:
    path = _active_path()
    if not os.path.exists(path):
        return False
    try:
        os.remove(path)
        return True
    except Exception as e:
        print(f"[storage] Error deleting active dataset: {e}")
        return False

def move_active_to_stored(new_name: str) -> bool:
    """
    Move the current active dataset into stored datasets (with a new name),
    and clear the active dataset slot.
    """
    active_path = _active_path()
    target_path = _dataset_path(new_name)
    
    if not os.path.exists(active_path):
        return False

    try:
        shutil.move(active_path, target_path)
        return True
    except Exception as e:
        print(f"[storage] Error moving active dataset to stored datasets: {e}")
        return False
