import pandas as pd
import os

DATASET_STORAGE = {}  # Temporary in-memory storage, but should be DB-backed

def save_dataset(name, data):
    """Save dataset efficiently using Parquet (faster than CSV)."""
    file_path = f"datasets/{name}.parquet"
    df = pd.DataFrame(data)
    df.to_parquet(file_path, compression="snappy")
    DATASET_STORAGE[name] = file_path  # Store reference to file
    return file_path

def get_dataset(name, chunk_size=None):
    """Load dataset in chunks to reduce memory usage."""
    file_path = DATASET_STORAGE.get(name)
    if not file_path or not os.path.exists(file_path):
        return None

    if chunk_size:
        return pd.read_parquet(file_path, engine="pyarrow", chunksize=chunk_size)  # Load in chunks
    return pd.read_parquet(file_path, engine="pyarrow")
