from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from .factory import TransformationFactory

class BaseTransformationProcessor(ABC):
    """Base class for all transformation processors"""
    
    @abstractmethod
    def transform(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Transform the dataframe according to the processor's logic
        
        Args:
            df (pd.DataFrame): The input dataframe
            **kwargs: Additional parameters specific to the transformation
            
        Returns:
            pd.DataFrame: The transformed dataframe
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the transformation"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the transformation does"""
        pass

    @property
    @abstractmethod
    def parameters(self) -> dict:
        """
        Return a dictionary of required parameters and their descriptions
        
        Returns:
            dict: Dictionary of parameter names and their descriptions
            Example: {
                'column': 'The column to transform',
                'value': 'The value to use in transformation'
            }
        """
        pass

# 🔥 Default Transformations
class NormalizeProcessor(BaseTransformationProcessor):
    """Applies Min-Max normalization"""
    def transform(self, df, column):
        df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
        return df

    @property
    def name(self) -> str:
        return "NormalizeProcessor"

    @property
    def description(self) -> str:
        return "Applies Min-Max normalization"

    @property
    def parameters(self) -> dict:
        return {
            'column': 'The column to transform'
        }

class LogProcessor(BaseTransformationProcessor):
    """Applies logarithm transformation"""
    def transform(self, df, column):
        df[column] = np.log1p(df[column])  # Avoids log(0) issue
        return df

    @property
    def name(self) -> str:
        return "LogProcessor"

    @property
    def description(self) -> str:
        return "Applies logarithm transformation"

    @property
    def parameters(self) -> dict:
        return {
            'column': 'The column to transform'
        }

class SquareRootProcessor(BaseTransformationProcessor):
    """Applies square root transformation"""
    def transform(self, df, column):
        df[column] = np.sqrt(df[column])
        return df

    @property
    def name(self) -> str:
        return "SquareRootProcessor"

    @property
    def description(self) -> str:
        return "Applies square root transformation"

    @property
    def parameters(self) -> dict:
        return {
            'column': 'The column to transform'
        }
