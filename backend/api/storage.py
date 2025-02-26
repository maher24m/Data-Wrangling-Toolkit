import pandas as pd

# Global storage for datasets (use a database in production)
DATASET_STORAGE = {}

def get_dataset(dataset_name):
    """Retrieve a dataset if it exists"""
    return DATASET_STORAGE.get(dataset_name, None)

def save_dataset(dataset_name, df):
    """Save a dataset into storage"""
    DATASET_STORAGE[dataset_name] = df

def delete_dataset(dataset_name):
    """Remove a dataset from storage"""
    if dataset_name in DATASET_STORAGE:
        del DATASET_STORAGE[dataset_name]

def list_datasets():
    """Return a list of all stored datasets"""
    return list(DATASET_STORAGE.keys())
