import pandas as pd
import numpy as np
from ..base import BaseTransformation
from ..properties.normalize import NORMALIZE_PROPERTIES

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