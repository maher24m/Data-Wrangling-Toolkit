import pandas as pd
import numpy as np

class TransformationProcessor:
    """Base class for all transformation processors"""
    def apply(self, df, column):
        raise NotImplementedError("Subclasses must implement this method")

# 🔥 Default Transformations
class NormalizeProcessor(TransformationProcessor):
    """Applies Min-Max normalization"""
    def apply(self, df, column):
        df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
        return df

class LogProcessor(TransformationProcessor):
    """Applies logarithm transformation"""
    def apply(self, df, column):
        df[column] = np.log1p(df[column])  # Avoids log(0) issue
        return df

class SquareRootProcessor(TransformationProcessor):
    """Applies square root transformation"""
    def apply(self, df, column):
        df[column] = np.sqrt(df[column])
        return df
