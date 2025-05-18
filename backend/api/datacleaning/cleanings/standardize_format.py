import pandas as pd
from ..base import BaseCleaning

STANDARDIZE_FORMAT_PROPERTIES = {
    'name': 'standardize_format',
    'description': 'Standardizes the format of date and numeric columns',
    'parameters': {
        'date_columns': 'List of columns to convert to datetime format',
        'number_columns': 'List of columns to convert to numeric format'
    }
}

class StandardizeFormatCleaning(BaseCleaning):
    def clean(self, df: pd.DataFrame, date_columns: list = None, number_columns: list = None) -> pd.DataFrame:
        df_copy = df.copy()

        if date_columns:
            for c in date_columns:
                if c in df_copy.columns:
                    # errors='coerce' will turn unparseable dates into NaT (Not a Time)
                    df_copy[c] = pd.to_datetime(df_copy[c], errors="coerce")
                else:
                    print(f"Warning: Date column '{c}' not found in DataFrame.")

        if number_columns:
            for c in number_columns:
                if c in df_copy.columns:
                    # errors='coerce' will turn unparseable numbers into NaN
                    df_copy[c] = pd.to_numeric(df_copy[c], errors="coerce")
                else:
                    print(f"Warning: Number column '{c}' not found in DataFrame.")

        return df_copy

    @property
    def name(self) -> str:
        return STANDARDIZE_FORMAT_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return STANDARDIZE_FORMAT_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return STANDARDIZE_FORMAT_PROPERTIES['parameters'] 