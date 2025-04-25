import pandas as pd

class CleaningProcessor:
    """Base class for all data cleaning processors"""
    def apply(self, df):
        """
        Apply the cleaning operation to the dataframe
        
        Args:
            df (pandas.DataFrame): The dataframe to clean
            
        Returns:
            pandas.DataFrame: The cleaned dataframe
        """
        raise NotImplementedError("Subclasses must implement this method")

# Default Cleaning Processors
class RemoveNullsProcessor(CleaningProcessor):
    """Removes rows with null values"""
    def apply(self, df):
        return df.dropna()

class RemoveDuplicatesProcessor(CleaningProcessor):
    """Removes duplicate rows"""
    def apply(self, df):
        return df.drop_duplicates()

class FillNullsProcessor(CleaningProcessor):
    """Fills null values with a specified value"""
    def apply(self, df, value=None, method=None, columns=None):
        if columns:
            if method:
                return df[columns].fillna(method=method)
            else:
                return df[columns].fillna(value=value)
        else:
            if method:
                return df.fillna(method=method)
            else:
                return df.fillna(value=value)

class ReplaceValuesProcessor(CleaningProcessor):
    """Replaces specific values in the dataframe"""
    def apply(self, df, to_replace, value, columns=None):
        if columns:
            return df[columns].replace(to_replace=to_replace, value=value)
        else:
            return df.replace(to_replace=to_replace, value=value) 