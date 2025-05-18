import pandas as pd
import numpy as np
from ..base import BaseAnalysis

DESCRIPTIVE_PROPERTIES = {
    'name': 'descriptive',
    'description': 'Provides basic statistical descriptions of numeric columns',
    'parameters': {
        'columns': 'List of columns to analyze (optional, defaults to all numeric columns)',
        'include_categorical': 'Whether to include categorical columns (default: False)'
    }
}

class DescriptiveAnalysis(BaseAnalysis):
    def analyze(self, df: pd.DataFrame, columns: list = None, include_categorical: bool = False) -> dict:
        """
        Analyze the dataframe and return descriptive statistics
        
        Args:
            df (pd.DataFrame): The input dataframe
            columns (list, optional): List of columns to analyze
            include_categorical (bool): Whether to include categorical columns
            
        Returns:
            dict: Dictionary containing descriptive statistics
        """
        # Select columns to analyze
        if columns is None:
            if include_categorical:
                columns = df.columns
            else:
                columns = df.select_dtypes(include=[np.number]).columns
        
        # Validate columns
        invalid_cols = [col for col in columns if col not in df.columns]
        if invalid_cols:
            raise ValueError(f"Columns not found in dataframe: {invalid_cols}")
        
        # Calculate statistics for numeric columns
        numeric_cols = df[columns].select_dtypes(include=[np.number]).columns
        numeric_stats = {}
        if len(numeric_cols) > 0:
            numeric_stats = df[numeric_cols].describe().to_dict()
        
        # Calculate statistics for categorical columns
        categorical_cols = df[columns].select_dtypes(include=['object', 'category']).columns
        categorical_stats = {}
        if len(categorical_cols) > 0:
            for col in categorical_cols:
                value_counts = df[col].value_counts()
                categorical_stats[col] = {
                    'unique_values': len(value_counts),
                    'most_common': value_counts.head(5).to_dict(),
                    'missing_values': df[col].isna().sum()
                }
        
        return {
            'numeric_columns': numeric_stats,
            'categorical_columns': categorical_stats,
            'total_rows': len(df),
            'total_columns': len(columns)
        }
    
    @property
    def name(self) -> str:
        return DESCRIPTIVE_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return DESCRIPTIVE_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return DESCRIPTIVE_PROPERTIES['parameters'] 