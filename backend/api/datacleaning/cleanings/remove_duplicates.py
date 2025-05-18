import pandas as pd
from ..base import BaseCleaning

REMOVE_DUPLICATES_PROPERTIES = {
    'name': 'remove_duplicates',
    'description': 'Removes duplicate rows from the dataset',
    'parameters': {
        'columns': 'Optional list of columns to consider for duplicates. If not provided, considers all columns',
        'keep': 'Which duplicate to keep (first, last, or False to drop all)'
    }
}

class RemoveDuplicatesCleaning(BaseCleaning):
    def clean(self, df: pd.DataFrame, columns: list = None, keep: str = 'first') -> pd.DataFrame:
        if keep not in ["first", "last", False]:
            raise ValueError("Invalid 'keep' parameter. Must be 'first', 'last', or False.")

        # Filter for columns that actually exist
        valid_cols = None
        if columns is not None:
            valid_cols = [col for col in columns if col in df.columns]
            if not valid_cols and columns:  # If columns were specified but none were valid
                print(f"Warning: No valid columns found for duplicate removal from {columns}. Checking all columns.")
                valid_cols = None  # Revert to checking all columns

        return df.drop_duplicates(subset=valid_cols, keep=keep)

    @property
    def name(self) -> str:
        return REMOVE_DUPLICATES_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return REMOVE_DUPLICATES_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return REMOVE_DUPLICATES_PROPERTIES['parameters'] 