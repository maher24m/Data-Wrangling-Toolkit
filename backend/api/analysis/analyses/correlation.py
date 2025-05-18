import pandas as pd
import numpy as np
from ..base import BaseAnalysis

CORRELATION_PROPERTIES = {
    'name': 'correlation',
    'description': 'Analyzes correlations between numeric columns',
    'parameters': {
        'columns': 'List of columns to analyze (optional, defaults to all numeric columns)',
        'method': 'Correlation method: pearson, kendall, or spearman (default: pearson)',
        'min_correlation': 'Minimum correlation value to include in results (default: 0.1)'
    }
}

class CorrelationAnalysis(BaseAnalysis):
    def analyze(self, df: pd.DataFrame, columns: list = None, method: str = 'pearson', min_correlation: float = 0.1) -> dict:
        """
        Analyze correlations between numeric columns
        
        Args:
            df (pd.DataFrame): The input dataframe
            columns (list, optional): List of columns to analyze
            method (str): Correlation method (pearson, kendall, or spearman)
            min_correlation (float): Minimum correlation value to include
            
        Returns:
            dict: Dictionary containing correlation analysis results
        """
        # Select columns to analyze
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        # Validate columns
        invalid_cols = [col for col in columns if col not in df.columns]
        if invalid_cols:
            raise ValueError(f"Columns not found in dataframe: {invalid_cols}")
        
        # Calculate correlation matrix
        corr_matrix = df[columns].corr(method=method)
        
        # Get significant correlations
        significant_correlations = []
        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= min_correlation:
                    significant_correlations.append({
                        'column1': columns[i],
                        'column2': columns[j],
                        'correlation': corr_value,
                        'strength': 'strong' if abs(corr_value) > 0.7 else 'moderate' if abs(corr_value) > 0.3 else 'weak'
                    })
        
        # Sort correlations by absolute value
        significant_correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        return {
            'correlation_matrix': corr_matrix.to_dict(),
            'significant_correlations': significant_correlations,
            'method': method,
            'total_columns': len(columns),
            'total_correlations': len(significant_correlations)
        }
    
    @property
    def name(self) -> str:
        return CORRELATION_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return CORRELATION_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return CORRELATION_PROPERTIES['parameters'] 