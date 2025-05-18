import pandas as pd
import numpy as np
from ..base import BaseCleaning

MISSING_VALUES_PROPERTIES = {
    'name': 'missing_values',
    'description': 'Handles missing values in the dataset using various methods',
    'parameters': {
        'method': 'The method to handle missing values (mean, median, mode, constant, remove)',
        'columns': 'Optional list of columns to process. If not provided, processes all columns',
        'value': 'Required only for constant method - the value to fill missing values with',
        'how': 'For remove method - how to determine which rows to remove (any/all)'
    }
}

class MissingValuesCleaning(BaseCleaning):
    def clean(self, df: pd.DataFrame, method: str, columns: list = None, value = None, how: str = 'any') -> pd.DataFrame:
        if not method:
            raise ValueError("Missing 'method' parameter for missing values cleaning.")

        # Use all columns if 'columns' is not provided or None
        cols_to_process = columns if columns is not None else df.columns

        # Filter for columns that actually exist in the DataFrame
        valid_cols = [col for col in cols_to_process if col in df.columns]
        if not valid_cols:
            print(f"Warning: No valid columns found for missing value imputation from {cols_to_process}")
            return df

        df_copy = df.copy()

        if method == "mean":
            for c in valid_cols:
                # Apply only to numeric columns for mean/median
                if pd.api.types.is_numeric_dtype(df_copy[c]):
                    fill_value = df_copy[c].mean()
                    if not pd.isna(fill_value):  # Check if mean is calculable
                        df_copy[c] = df_copy[c].fillna(fill_value)
                    else:
                        print(f"Warning: Cannot compute mean for column '{c}'. Skipping fillna.")
                else:
                    print(f"Warning: Column '{c}' is not numeric. Skipping mean imputation.")
        elif method == "median":
            for c in valid_cols:
                if pd.api.types.is_numeric_dtype(df_copy[c]):
                    fill_value = df_copy[c].median()
                    if not pd.isna(fill_value):  # Check if median is calculable
                        df_copy[c] = df_copy[c].fillna(fill_value)
                    else:
                        print(f"Warning: Cannot compute median for column '{c}'. Skipping fillna.")
                else:
                    print(f"Warning: Column '{c}' is not numeric. Skipping median imputation.")
        elif method == "mode":
            for c in valid_cols:
                m = df_copy[c].mode()
                if not m.empty:
                    df_copy[c] = df_copy[c].fillna(m[0])
        elif method == "constant":
            if value is None:
                raise ValueError("'constant' replacement requires a 'value' parameter.")
            # fillna with dict only applies to specified columns
            fill_dict = {c: value for c in valid_cols}
            df_copy = df_copy.fillna(value=fill_dict)
        elif method == "remove":
            df_copy = df_copy.dropna(how=how, subset=valid_cols)
        else:
            raise ValueError(f"Unknown method '{method}' for missing_values")
        return df_copy

    @property
    def name(self) -> str:
        return MISSING_VALUES_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return MISSING_VALUES_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return MISSING_VALUES_PROPERTIES['parameters'] 