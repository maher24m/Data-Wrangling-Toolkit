# api/datasets/manager.py

import pandas as pd
import os
from api.storage import (
    get_dataset as _load,
    save_dataset as _save,
    list_datasets as _list,
    save_active_dataset as _save_active,
    get_active_dataset as _load_active,
    list_datasets as _list_stored,
    move_active_to_stored as _move_active,
    delete_active_dataset as _delete_active,
)

_active_dataset_name = None  # Only track the *name* now if moved

def save_dataset(name, data):
    if isinstance(data, pd.DataFrame):
        data = data.to_dict(orient="records")
    return _save(name, data)

def get_dataset(name, chunk_size=None):
    if chunk_size:
        paths = _list_stored()
        if name not in paths:
            return None
        file_path = os.path.join("stored_datasets", f"{name}.parquet")
        if not os.path.exists(file_path):
            return None
        return pd.read_parquet(file_path, engine="pyarrow", chunksize=chunk_size)
    return _load(name)

def list_datasets():
    return _list_stored()

def set_active_dataset_from_stored(name):
    """
    Set a dataset from stored datasets as the new active dataset.
    This will move the selected dataset to active_dataset/active.parquet
    """
    global _active_dataset_name

    if name not in _list_stored():
        return False
    
    # Load dataset from stored datasets
    df = _load(name)
    if df is None:
        return False

    # Save as active
    _save_active(df)
    _active_dataset_name = name
    return True

def import_new_active_dataset(data):
    """
    When a user uploads a fresh new dataset (NOT from stored ones).
    Replace current active and clear active name.
    """
    global _active_dataset_name

    _delete_active()
    _save_active(data)
    _active_dataset_name = None  # No name yet; it's a temporary active dataset

def get_active_dataset():
    return _load_active()

def get_active_dataset_name():
    return _active_dataset_name

def archive_active_dataset(new_name):
    """
    Move the current active dataset into stored datasets under a given name.
    """
    global _active_dataset_name

    success = _move_active(new_name)
    if success:
        _active_dataset_name = new_name
    return success
