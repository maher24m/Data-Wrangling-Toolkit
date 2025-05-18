from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd

class BaseAnalysis(ABC):
    """Base class for all analyses"""
    
    @abstractmethod
    def analyze(self, df: pd.DataFrame, **kwargs) -> Dict[str, Any]:
        """
        Analyze the dataframe according to the analysis's logic
        
        Args:
            df (pd.DataFrame): The input dataframe
            **kwargs: Additional parameters specific to the analysis
            
        Returns:
            Dict[str, Any]: The analysis results
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the analysis"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the analysis does"""
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