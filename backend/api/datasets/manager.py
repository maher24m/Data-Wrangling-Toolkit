# api/datasets/manager.py

import pandas as pd
import os
from api.storage import (
    get_dataset as _load,
    save_dataset as _save,
    delete_dataset as _delete,
    list_datasets as _list_stored,

)

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

def delete_dataset(name):
    return _delete(name)
