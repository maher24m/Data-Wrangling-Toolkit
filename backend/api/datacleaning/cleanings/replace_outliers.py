import pandas as pd
import numpy as np
from ..base import BaseCleaning
from .detect_outliers import DetectOutliersCleaning

REPLACE_OUTLIERS_PROPERTIES = {
    'name': 'replace_outliers',
    'description': 'Replaces detected outliers with statistical values',
    'parameters': {
        'method': 'The method to detect outliers (std or iqr)',
        'n_std': 'Number of standard deviations for std method (default: 3.0)',
        'replace_with': 'The method to replace outliers (mean, median, or mode)',
        'columns': 'Optional list of columns to process. If not provided, processes all numeric columns'
    }
}

class ReplaceOutliersCleaning(BaseCleaning):
    def clean(self, df: pd.DataFrame, method: str = 'std', n_std: float = 3.0, replace_with: str = 'mean', columns: list = None) -> pd.DataFrame:
        if replace_with not in ["mean", "median", "mode"]:
            raise ValueError("Invalid 'replace_with' parameter. Must be 'mean', 'median', or 'mode'.")

        # Use the detection processor to flag outliers
        detection_params = {"method": method, "n_std": n_std, "columns": columns}
        flagged_df = DetectOutliersCleaning().clean(df, **detection_params)

        if "_is_outlier" not in flagged_df.columns:
            print("Warning: '_is_outlier' column not found after detection step.")
            return df

        mask = flagged_df["_is_outlier"]
        df_copy = df.copy()

        # Determine columns to process (same logic as detection)
        cols_to_process = columns if columns is not None else df.select_dtypes(include=np.number).columns
        valid_cols = [
            col for col in cols_to_process
            if col in df_copy.columns and pd.api.types.is_numeric_dtype(df_copy[col])
        ]

        if not valid_cols:
            print(f"Warning: No valid numeric columns found for outlier replacement from {cols_to_process}")
            if "_is_outlier" in flagged_df.columns:
                return flagged_df.drop(columns=["_is_outlier"])
            else:
                return df

        # compute replacement stats based on the *original* non-outlier data
        stats = {}
        for c in valid_cols:
            # Select non-outlier values for calculating replacement stat
            non_outlier_values = df_copy.loc[~mask, c].dropna()
            if non_outlier_values.empty:
                print(f"Warning: No non-outlier values found for column '{c}'. Cannot compute replacement stat. Skipping replacement.")
                stats[c] = None
                continue

            if replace_with == "mean":
                stats[c] = non_outlier_values.mean()
            elif replace_with == "median":
                stats[c] = non_outlier_values.median()
            elif replace_with == "mode":
                m = non_outlier_values.mode()
                # Use mean as fallback if mode is empty or not calculable
                stats[c] = m[0] if not m.empty else non_outlier_values.mean()

            if pd.isna(stats[c]):
                print(f"Warning: Could not compute '{replace_with}' for column '{c}'. Skipping replacement.")
                stats[c] = None

        # Apply replacement only where mask is True and stat is calculable
        for c in valid_cols:
            if stats[c] is not None:
                df_copy.loc[mask, c] = stats[c]

        return df_copy

    @property
    def name(self) -> str:
        return REPLACE_OUTLIERS_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return REPLACE_OUTLIERS_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return REPLACE_OUTLIERS_PROPERTIES['parameters'] 