# api/datasets/manager.py

import pandas as pd
import os
from api.storage import get_dataset as _load, save_dataset as _save, list_datasets as _list

_active_dataset = None

def save_dataset(name, data):
    if isinstance(data, pd.DataFrame):
        data = data.to_dict(orient="records")
    return _save(name, data)

def get_dataset(name, chunk_size=None):
    if chunk_size:
        paths = _list()
        file_path = paths.get(name)
        if not file_path or not os.path.exists(file_path):
            return None
        return pd.read_parquet(file_path, engine="pyarrow", chunksize=chunk_size)
    return _load(name)

def list_datasets():
    return _list()

def set_active_dataset(name):
    global _active_dataset
    if name in _list():
        _active_dataset = name

def get_active_dataset():
    if _active_dataset:
        return get_dataset(_active_dataset)
    return None

def get_active_dataset_name():
    return _active_dataset if _active_dataset else None
