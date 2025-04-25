import pandas as pd
import numpy as np
from api.datacleaning.processor import CleaningProcessor

class OutlierRemovalProcessor(CleaningProcessor):
    """
    Removes outliers from specified columns using the IQR method
    """
    # This attribute is used by the plugin loader to identify the operation type
    operation_type = "remove_outliers"
    
    def apply(self, df, columns=None, threshold=1.5):
        """
        Remove outliers from specified columns using the IQR method
        
        Args:
            df (pandas.DataFrame): The dataframe to clean
            columns (list): List of column names to process. If None, process all numeric columns
            threshold (float): IQR multiplier for outlier detection (default: 1.5)
            
        Returns:
            pandas.DataFrame: The dataframe with outliers removed
        """
        # If no columns specified, use all numeric columns
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Create a mask for rows to keep
        mask = pd.Series(True, index=df.index)
        
        for column in columns:
            if column not in df.columns:
                continue
                
            # Calculate Q1, Q3 and IQR
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define bounds
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            # Update mask to keep rows within bounds
            column_mask = (df[column] >= lower_bound) & (df[column] <= upper_bound)
            mask = mask & column_mask
        
        # Return dataframe with outliers removed
        return df[mask] 