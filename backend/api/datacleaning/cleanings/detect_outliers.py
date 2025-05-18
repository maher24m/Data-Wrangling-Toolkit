import pandas as pd
import numpy as np
from ..base import BaseCleaning

DETECT_OUTLIERS_PROPERTIES = {
    'name': 'detect_outliers',
    'description': 'Detects outliers in numeric columns using statistical methods',
    'parameters': {
        'method': 'The method to detect outliers (std or iqr)',
        'n_std': 'Number of standard deviations for std method (default: 3.0)',
        'columns': 'Optional list of columns to process. If not provided, processes all numeric columns'
    }
}

class DetectOutliersCleaning(BaseCleaning):
    def clean(self, df: pd.DataFrame, method: str = 'std', n_std: float = 3.0, columns: list = None) -> pd.DataFrame:
        if method not in ["std", "iqr"]:
            raise ValueError("Invalid 'method' parameter. Must be 'std' or 'iqr'.")

        cols_to_process = columns if columns is not None else df.select_dtypes(include=np.number).columns
        # Filter for valid numeric columns that exist
        valid_cols = [
            col for col in cols_to_process
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col])
        ]

        if not valid_cols:
            print(f"Warning: No valid numeric columns found for outlier detection from {cols_to_process}")
            # Add the column anyway, but all False
            df_copy = df.copy()
            df_copy["_is_outlier"] = False
            return df_copy

        df_copy = df.copy()
        # Initialize mask
        mask = pd.Series(False, index=df_copy.index)

        if method == "std":
            for c in valid_cols:
                # Skip columns with no variance
                s = df_copy[c].std()
                if pd.isna(s) or s == 0:
                    print(f"Warning: Skipping outlier detection for column '{c}' (std is NaN or zero).")
                    continue
                m = df_copy[c].mean()
                lower_bound = m - n_std * s
                upper_bound = m + n_std * s
                mask |= (df_copy[c] < lower_bound) | (df_copy[c] > upper_bound)
        elif method == "iqr":
            for c in valid_cols:
                q1 = df_copy[c].quantile(0.25)
                q3 = df_copy[c].quantile(0.75)
                # Skip if quantiles are NaN (e.g., all NaNs in column)
                if pd.isna(q1) or pd.isna(q3):
                    print(f"Warning: Skipping outlier detection for column '{c}' (cannot compute Q1/Q3).")
                    continue
                iqr = q3 - q1
                # Skip if IQR is zero (no variability in the middle 50%)
                if iqr == 0:
                    print(f"Warning: Skipping outlier detection for column '{c}' (IQR is zero).")
                    continue
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                mask |= (df_copy[c] < lower_bound) | (df_copy[c] > upper_bound)

        df_copy["_is_outlier"] = mask
        return df_copy

    @property
    def name(self) -> str:
        return DETECT_OUTLIERS_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return DETECT_OUTLIERS_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return DETECT_OUTLIERS_PROPERTIES['parameters'] 