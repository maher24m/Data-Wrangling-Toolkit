from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd

class BaseTransformation(ABC):
    """Base class for all transformations"""
    
    @abstractmethod
    def transform(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Transform the dataframe according to the transformation's logic
        
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
    def parameters(self) -> Dict[str, str]:
        """
        Return a dictionary of required parameters and their descriptions
        
        Returns:
            Dict[str, str]: Dictionary of parameter names and their descriptions
        """
        pass 