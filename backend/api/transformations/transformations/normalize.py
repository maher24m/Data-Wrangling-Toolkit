import pandas as pd
import numpy as np
from ..base import BaseTransformation


NORMALIZE_PROPERTIES = {
    'name': 'normalize',
    'description': 'Applies Min-Max normalization (scales values between 0 and 1)',
    'parameters': {
        'column': 'The column to transform',
        'range_min': 'Minimum value for scaling (default: 0)',
        'range_max': 'Maximum value for scaling (default: 1)'
    }
} 
class NormalizeTransformation(BaseTransformation):
    def transform(self, df: pd.DataFrame, column: str, range_min: float = 0, range_max: float = 1) -> pd.DataFrame:
        df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
        df[column] = df[column] * (range_max - range_min) + range_min
        return df
    
    @property
    def name(self) -> str:
        return NORMALIZE_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return NORMALIZE_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return NORMALIZE_PROPERTIES['parameters'] 