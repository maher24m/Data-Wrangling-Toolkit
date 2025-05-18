from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd

class BaseCleaning(ABC):
    """Base class for all data cleaning operations"""
    
    @abstractmethod
    def clean(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Clean the dataframe according to the cleaning operation's logic
        
        Args:
            df (pd.DataFrame): The input dataframe
            **kwargs: Additional parameters specific to the cleaning operation
            
        Returns:
            pd.DataFrame: The cleaned dataframe
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the cleaning operation"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the cleaning operation does"""
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