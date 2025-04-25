import pandas as pd
import os
from api.storage import get_dataset, save_dataset, list_datasets

ACTIVE_DATASET = None  # Stores active dataset name

class DatasetManager:
    """Handles dataset-specific operations and active dataset management"""

    @staticmethod
    def save_dataset(name, data):
        """Save dataset using the storage system."""
        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient="records")
        return save_dataset(name, data)

    @staticmethod
    def get_dataset(name, chunk_size=None):
        """Load dataset with optional chunking support."""
        if chunk_size:
            file_path = list_datasets().get(name)
            if not file_path or not os.path.exists(file_path):
                return None
            return pd.read_parquet(file_path, engine="pyarrow", chunksize=chunk_size)
        return get_dataset(name)

    @staticmethod
    def list_datasets():
        """Return a list of available datasets using the storage module."""
        return list_datasets()

    @staticmethod
    def set_active_dataset(name):
        """Set the active dataset for transformations & processing."""
        global ACTIVE_DATASET
        if name in list_datasets():
            ACTIVE_DATASET = name

    @staticmethod
    def get_active_dataset():
        """Retrieve the currently active dataset."""
        if ACTIVE_DATASET:
            return DatasetManager.get_dataset(ACTIVE_DATASET)
        return None
