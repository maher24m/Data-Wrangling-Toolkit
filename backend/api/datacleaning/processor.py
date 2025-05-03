# backend/api/datacleaning/processor.py
import pandas as pd
import numpy as np # Import numpy for isnan check if needed later

# --- FIX: Rename base class ---
class DataCleaningProcessor:
    """Base class / interface for all data cleaning processors."""
    # Optional: Define a class attribute for the operation name, useful for plugins
    # operation_name = None

    def apply(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        """
        Applies the cleaning operation to the DataFrame.
        Subclasses must implement this method.
        Parameters should be extracted from the 'params' dict.
        """
        raise NotImplementedError


# --- FIX: Inherit from DataCleaningProcessor and fix apply signature ---
class MissingValuesCleaner(DataCleaningProcessor):
    # operation_name = "missing_values" # Example if needed for discovery

    def apply(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        method = params.get("method")
        columns = params.get("columns") # Optional, defaults to all columns later
        value = params.get("value") # Required only for 'constant' method

        if not method:
            raise ValueError("Missing 'method' parameter for missing values cleaning.")

        # Use all columns if 'columns' is not provided or None
        cols_to_process = columns if columns is not None else df.columns

        # Filter for columns that actually exist in the DataFrame
        valid_cols = [col for col in cols_to_process if col in df.columns]
        if not valid_cols:
            # Return original df if no valid columns specified or found
            # Or raise an error? For now, let's return df.
            print(f"Warning: No valid columns found for missing value imputation from {cols_to_process}")
            return df

        df_copy = df.copy() # Work on a copy to avoid modifying original df inplace unexpectedly

        if method == "mean":
            for c in valid_cols:
                 # Apply only to numeric columns for mean/median
                if pd.api.types.is_numeric_dtype(df_copy[c]):
                    fill_value = df_copy[c].mean()
                    if not pd.isna(fill_value): # Check if mean is calculable
                         df_copy[c] = df_copy[c].fillna(fill_value)
                    else:
                         print(f"Warning: Cannot compute mean for column '{c}'. Skipping fillna.")
                else:
                    print(f"Warning: Column '{c}' is not numeric. Skipping mean imputation.")
        elif method == "median":
            for c in valid_cols:
                if pd.api.types.is_numeric_dtype(df_copy[c]):
                    fill_value = df_copy[c].median()
                    if not pd.isna(fill_value): # Check if median is calculable
                         df_copy[c] = df_copy[c].fillna(fill_value)
                    else:
                         print(f"Warning: Cannot compute median for column '{c}'. Skipping fillna.")

                else:
                    print(f"Warning: Column '{c}' is not numeric. Skipping median imputation.")
        elif method == "mode":
            for c in valid_cols:
                m = df_copy[c].mode()
                if not m.empty:
                    df_copy[c] = df_copy[c].fillna(m[0])
                # else: No mode found, leave NaNs as they are
        elif method == "constant":
            if value is None:
                raise ValueError("'constant' replacement requires a 'value' parameter.")
            # fillna with dict only applies to specified columns
            fill_dict = {c: value for c in valid_cols}
            df_copy = df_copy.fillna(value=fill_dict)
        # --- FIX: Add remove method ---
        elif method == "remove":
            how = params.get("how", "any") # Default 'any'
            df_copy = df_copy.dropna(how=how, subset=valid_cols)
        else:
            raise ValueError(f"Unknown method '{method}' for missing_values")
        return df_copy


# --- FIX: Inherit from DataCleaningProcessor and fix apply signature ---
class RemoveDuplicatesCleaner(DataCleaningProcessor):
    # operation_name = "remove_duplicates"

    def apply(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        columns = params.get("columns") # Optional, defaults to all columns
        keep = params.get("keep", "first") # Default 'first'

        if keep not in ["first", "last", False]:
             raise ValueError("Invalid 'keep' parameter. Must be 'first', 'last', or False.")

        # Filter for columns that actually exist
        valid_cols = None
        if columns is not None:
            valid_cols = [col for col in columns if col in df.columns]
            if not valid_cols and columns: # If columns were specified but none were valid
                 print(f"Warning: No valid columns found for duplicate removal from {columns}. Checking all columns.")
                 valid_cols = None # Revert to checking all columns

        return df.drop_duplicates(subset=valid_cols, keep=keep)


# --- NOTE: RemoveMissingCleaner is now handled by MissingValuesCleaner with method="remove" ---
# --- Keep RemoveMissingDataProcessor class name for factory compatibility if needed, ---
# --- but point it to MissingValuesCleaner implementation logic. Or update factory ---
# --- Let's keep it simple and remove this class, updating the factory ---
# class RemoveMissingCleaner(DataCleaningProcessor): ... (REMOVED)


# --- FIX: Inherit from DataCleaningProcessor and fix apply signature ---
# --- FIX: Standardize outlier column name ---
class DetectOutliersCleaner(DataCleaningProcessor):
    # operation_name = "detect_outliers"

    def apply(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        method = params.get("method", "std") # Default 'std'
        n_std = params.get("n_std", 3.0) # Default 3
        columns = params.get("columns") # Optional, defaults to numeric columns

        if method not in ["std", "iqr"]:
            raise ValueError("Invalid 'method' parameter. Must be 'std' or 'iqr'.")

        cols_to_process = columns if columns is not None else df.select_dtypes(include=np.number).columns
        # Filter for valid numeric columns that exist
        valid_cols = [
            col for col in cols_to_process
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col])
        ]

        if not valid_cols:
            print(f"Warning: No valid numeric columns found for outlier detection from {cols_to_process}")
            # Add the column anyway, but all False
            df_copy = df.copy()
            df_copy["_is_outlier"] = False
            return df_copy

        df_copy = df.copy()
        # Initialize mask
        mask = pd.Series(False, index=df_copy.index)

        if method == "std":
            for c in valid_cols:
                # Skip columns with no variance
                s = df_copy[c].std()
                if pd.isna(s) or s == 0:
                     print(f"Warning: Skipping outlier detection for column '{c}' (std is NaN or zero).")
                     continue
                m = df_copy[c].mean()
                lower_bound = m - n_std * s
                upper_bound = m + n_std * s
                mask |= (df_copy[c] < lower_bound) | (df_copy[c] > upper_bound)
        elif method == "iqr":
            for c in valid_cols:
                q1 = df_copy[c].quantile(0.25)
                q3 = df_copy[c].quantile(0.75)
                # Skip if quantiles are NaN (e.g., all NaNs in column)
                if pd.isna(q1) or pd.isna(q3):
                    print(f"Warning: Skipping outlier detection for column '{c}' (cannot compute Q1/Q3).")
                    continue
                iqr = q3 - q1
                # Skip if IQR is zero (no variability in the middle 50%)
                if iqr == 0:
                    print(f"Warning: Skipping outlier detection for column '{c}' (IQR is zero).")
                    continue
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                mask |= (df_copy[c] < lower_bound) | (df_copy[c] > upper_bound)

        # --- FIX: Use consistent column name ---
        df_copy["_is_outlier"] = mask
        return df_copy


# --- FIX: Inherit from DataCleaningProcessor and fix apply signature ---
class ReplaceOutliersCleaner(DataCleaningProcessor):
    # operation_name = "replace_outliers"

    def apply(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        method = params.get("method", "std") # Default 'std' for detection
        n_std = params.get("n_std", 3.0) # Default 3 for detection
        replace_with = params.get("replace_with", "mean") # Default 'mean'
        columns = params.get("columns") # Optional, defaults to numeric columns

        if replace_with not in ["mean", "median", "mode"]:
             raise ValueError("Invalid 'replace_with' parameter. Must be 'mean', 'median', or 'mode'.")

        # Use the detection processor to flag outliers
        # Pass relevant detection params
        detection_params = {"method": method, "n_std": n_std, "columns": columns}
        flagged_df = DetectOutliersCleaner().apply(df, **detection_params)

        if "_is_outlier" not in flagged_df.columns:
             # Should not happen if DetectOutliersCleaner works correctly, but handle defensively
             print("Warning: '_is_outlier' column not found after detection step.")
             return df # Return original df

        mask = flagged_df["_is_outlier"]
        df_copy = df.copy() # Work on a copy of the original data

        # Determine columns to process (same logic as detection)
        cols_to_process = columns if columns is not None else df.select_dtypes(include=np.number).columns
        valid_cols = [
            col for col in cols_to_process
            if col in df_copy.columns and pd.api.types.is_numeric_dtype(df_copy[col])
        ]

        if not valid_cols:
            print(f"Warning: No valid numeric columns found for outlier replacement from {cols_to_process}")
            # Drop the temp column if it exists and return
            if "_is_outlier" in flagged_df.columns:
                 return flagged_df.drop(columns=["_is_outlier"])
            else:
                 return df

        # compute replacement stats based on the *original* non-outlier data
        stats = {}
        for c in valid_cols:
            # Select non-outlier values for calculating replacement stat
            non_outlier_values = df_copy.loc[~mask, c].dropna()
            if non_outlier_values.empty:
                 print(f"Warning: No non-outlier values found for column '{c}'. Cannot compute replacement stat. Skipping replacement.")
                 stats[c] = None # Mark as not calculable
                 continue

            if replace_with == "mean":
                stats[c] = non_outlier_values.mean()
            elif replace_with == "median":
                stats[c] = non_outlier_values.median()
            elif replace_with == "mode":
                m = non_outlier_values.mode()
                # Use mean as fallback if mode is empty or not calculable
                stats[c] = m[0] if not m.empty else non_outlier_values.mean()

            if pd.isna(stats[c]):
                 print(f"Warning: Could not compute '{replace_with}' for column '{c}'. Skipping replacement.")
                 stats[c] = None # Mark as not calculable


        # Apply replacement only where mask is True and stat is calculable
        for c in valid_cols:
             if stats[c] is not None:
                 # Apply replacement only to outliers in the specific column 'c'
                 # Need to consider only outliers relevant to *this* column if detection was column-specific?
                 # No, DetectOutliers creates a single mask based on all columns checked. So this is correct.
                 df_copy.loc[mask, c] = stats[c]


        # No need to drop "_is_outlier" as we worked on df_copy, not flagged_df
        return df_copy


# --- FIX: Inherit from DataCleaningProcessor and fix apply signature ---
class StandardizeFormatCleaner(DataCleaningProcessor):
    # operation_name = "standardize_format"

    def apply(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        date_columns = params.get("date_columns", [])
        number_columns = params.get("number_columns", [])

        df_copy = df.copy()

        for c in date_columns:
            if c in df_copy.columns:
                # errors='coerce' will turn unparseable dates into NaT (Not a Time)
                df_copy[c] = pd.to_datetime(df_copy[c], errors="coerce")
            else:
                print(f"Warning: Date column '{c}' not found in DataFrame.")

        for c in number_columns:
            if c in df_copy.columns:
                 # errors='coerce' will turn unparseable numbers into NaN
                df_copy[c] = pd.to_numeric(df_copy[c], errors="coerce")
            else:
                print(f"Warning: Number column '{c}' not found in DataFrame.")

        return df_copy


# --- FIX: Inherit from DataCleaningProcessor and fix apply signature ---
class ClusterSimilarCleaner(DataCleaningProcessor):
    # operation_name = "cluster_similar"

    def apply(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        column = params.get("column")
        # threshold = params.get("threshold", 0.8) # Example param

        if not column:
             raise ValueError("Missing 'column' parameter for cluster similar values.")
        if column not in df.columns:
             raise ValueError(f"Column '{column}' not found in DataFrame.")

        # stub – no-op for now
        print(f"Warning: 'cluster_similar' operation for column '{column}' is not yet implemented. Returning original DataFrame.")
        return df