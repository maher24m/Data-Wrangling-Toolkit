import pandas as pd
import numpy as np
from ..base import BaseTransformation

LOG_PROPERTIES = {
    'name': 'log',
    'description': 'Applies logarithm transformation',
    'parameters': {
        'column': 'The column to transform',
        'base': 'Log base: natural, 10, or 2',
        'handle_negatives': 'How to handle negative values: error, offset, or abs'
    }
} 
class LogTransformation(BaseTransformation):
    def transform(self, df: pd.DataFrame, column: str, base: str = 'natural', handle_negatives: str = 'error') -> pd.DataFrame:
        if handle_negatives == 'error' and (df[column] <= 0).any():
            raise ValueError("Column contains non-positive values")
            
        if base == 'natural':
            df[column] = np.log1p(df[column])
        elif base == '10':
            df[column] = np.log10(df[column] + 1)
        elif base == '2':
            df[column] = np.log2(df[column] + 1)
        return df
    
    @property
    def name(self) -> str:
        return LOG_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return LOG_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return LOG_PROPERTIES['parameters'] 