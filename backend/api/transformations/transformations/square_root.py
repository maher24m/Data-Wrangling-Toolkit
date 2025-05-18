import pandas as pd
import numpy as np
from ..base import BaseTransformation
from ..properties.square_root import SQUARE_ROOT_PROPERTIES

class SquareRootTransformation(BaseTransformation):
    def transform(self, df: pd.DataFrame, column: str, handle_negatives: str = 'error') -> pd.DataFrame:
        if handle_negatives == 'error' and (df[column] < 0).any():
            raise ValueError("Column contains negative values")
        elif handle_negatives == 'abs':
            df[column] = np.sqrt(df[column].abs())
        elif handle_negatives == 'zero':
            df[column] = np.sqrt(df[column].clip(lower=0))
        return df
    
    @property
    def name(self) -> str:
        return SQUARE_ROOT_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return SQUARE_ROOT_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return SQUARE_ROOT_PROPERTIES['parameters'] 