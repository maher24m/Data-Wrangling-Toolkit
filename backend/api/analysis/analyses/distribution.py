import pandas as pd
import numpy as np
from scipy import stats
from ..base import BaseAnalysis

DISTRIBUTION_PROPERTIES = {
    'name': 'distribution',
    'description': 'Analyzes the distribution of numeric columns',
    'parameters': {
        'columns': 'List of columns to analyze (optional, defaults to all numeric columns)',
        'bins': 'Number of bins for histogram (default: 10)',
        'test_normality': 'Whether to test for normal distribution (default: True)'
    }
}

class DistributionAnalysis(BaseAnalysis):
    def analyze(self, df: pd.DataFrame, columns: list = None, bins: int = 10, test_normality: bool = True) -> dict:
        """
        Analyze the distribution of numeric columns
        
        Args:
            df (pd.DataFrame): The input dataframe
            columns (list, optional): List of columns to analyze
            bins (int): Number of bins for histogram
            test_normality (bool): Whether to test for normal distribution
            
        Returns:
            dict: Dictionary containing distribution analysis results
        """
        # Select columns to analyze
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        # Validate columns
        invalid_cols = [col for col in columns if col not in df.columns]
        if invalid_cols:
            raise ValueError(f"Columns not found in dataframe: {invalid_cols}")
        
        results = {}
        for col in columns:
            # Skip columns with too many missing values
            if df[col].isna().sum() > len(df) * 0.5:
                results[col] = {
                    'error': 'Too many missing values for analysis'
                }
                continue
            
            # Calculate basic statistics
            stats_dict = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'skewness': df[col].skew(),
                'kurtosis': df[col].kurtosis(),
                'min': df[col].min(),
                'max': df[col].max(),
                'missing_values': df[col].isna().sum()
            }
            
            # Calculate histogram
            hist, bin_edges = np.histogram(df[col].dropna(), bins=bins)
            stats_dict['histogram'] = {
                'counts': hist.tolist(),
                'bin_edges': bin_edges.tolist()
            }
            
            # Test for normality if requested
            if test_normality:
                # Remove missing values for normality test
                clean_data = df[col].dropna()
                if len(clean_data) > 0:
                    # Perform Shapiro-Wilk test
                    shapiro_test = stats.shapiro(clean_data)
                    stats_dict['normality_test'] = {
                        'test': 'shapiro-wilk',
                        'statistic': shapiro_test.statistic,
                        'p_value': shapiro_test.pvalue,
                        'is_normal': shapiro_test.pvalue > 0.05
                    }
            
            results[col] = stats_dict
        
        return {
            'distributions': results,
            'total_columns': len(columns),
            'bins': bins,
            'tested_normality': test_normality
        }
    
    @property
    def name(self) -> str:
        return DISTRIBUTION_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return DISTRIBUTION_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return DISTRIBUTION_PROPERTIES['parameters'] 