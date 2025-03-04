import pandas as pd
import os

DATASET_STORAGE = {}
DATASET_PATH = "datasets/"
ACTIVE_DATASET = None  # Stores active dataset name

class DatasetManager:
    """Handles dataset storage and retrieval"""

    @staticmethod
    def save_dataset(name, data):
        """Save dataset as a Parquet file."""
        if not os.path.exists(DATASET_PATH):
            os.makedirs(DATASET_PATH)
        file_path = f"{DATASET_PATH}{name}.parquet"
        pd.DataFrame(data).to_parquet(file_path, compression="snappy")
        DATASET_STORAGE[name] = file_path
        return file_path

    @staticmethod
    def get_dataset(name, chunk_size=None):
        """Load dataset from Parquet file."""
        file_path = DATASET_STORAGE.get(name)
        if not file_path or not os.path.exists(file_path):
            return None
        if chunk_size:
            return pd.read_parquet(file_path, engine="pyarrow", chunksize=chunk_size)
        return pd.read_parquet(file_path, engine="pyarrow")

    @staticmethod
    def set_active_dataset(name):
        """Set the active dataset for transformations & processing."""
        global ACTIVE_DATASET
        if name in DATASET_STORAGE:
            ACTIVE_DATASET = name

    @staticmethod
    def get_active_dataset():
        """Retrieve the currently active dataset."""
        if ACTIVE_DATASET:
            return DatasetManager.get_dataset(ACTIVE_DATASET)
        return None
