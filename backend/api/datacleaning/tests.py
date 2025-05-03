# backend/api/datacleaning/tests.py
from django.test import TestCase, Client
from django.urls import reverse
import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

# --- FIX: Import specific processor for direct testing ---
from api.datacleaning.processor import MissingValuesCleaner, RemoveDuplicatesCleaner # Import processors you want to test directly

class DataCleaningTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Use a temporary directory for dataset files for cleaner tests
        self.test_dir = Path("./test_datasets")
        self.test_dir.mkdir(exist_ok=True)
        self.active_file_path = self.test_dir / "active.parquet"

        # Create a sample dataset
        self.sample_data = pd.DataFrame({
            'A': [1.0, 2.0, None, 4.0, 4.0, 100.0], # Use float for mean/median tests
            'B': ['a', 'b', 'b', None, 'e', 'e'],
            'C': [1.1, 2.2, 3.3, 4.4, 4.4, 1000.0],
            'date': ['2020-01-01', '2020/02/01', 'notadate', None, '2020-03-15', '2020-04-01'],
            'all_nan': [None, None, None, None, None, None] # Column for testing edge cases
        })
        # --- FIX: Mock dataset manager functions if they are complex ---
        # For simplicity here, we'll just write directly to the expected file path
        # assuming get_active_dataset reads from 'active.parquet' in some base dir
        # and get_active_dataset_name returns 'active'.
        # A better approach involves mocking api.datasets.manager functions.
        self.dataset_base_dir = Path('datasets') # Assume manager uses this base
        self.dataset_base_dir.mkdir(exist_ok=True)
        self.active_parquet_path = self.dataset_base_dir / 'active.parquet'
        self.sample_data.to_parquet(self.active_parquet_path)

    def tearDown(self):
        # Clean up test file
        try:
            os.remove(self.active_parquet_path)
        except OSError:
            pass
        # Remove base dir if empty? Better managed by test runner usually.
        # try:
        #     self.dataset_base_dir.rmdir() # Fails if not empty
        # except OSError:
        #     pass

    def _post_ops(self, ops):
        # Ensure ops is a list
        if not isinstance(ops, list):
            ops = [ops]
        return self.client.post(
            reverse('datacleaning:data-cleaning'),
            json.dumps({'operations': ops}), # Send as raw JSON body
            content_type='application/json'
        )

    def _reload(self):
        # Reload the dataset after operations
        try:
            return pd.read_parquet(self.active_parquet_path)
        except FileNotFoundError:
            return None # Return None if file doesn't exist

    # --- FIX: Update tests to use new 'type' keys and params ---

    def test_clean_missing_values_mean(self):
        resp = self._post_ops([{
            'type': 'missing_values', # Use consolidated type
            'method': 'mean',         # Specify method in params
            'columns': ['A']
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertIsNotNone(df)
        self.assertFalse(df['A'].isnull().any())
        # Check if the imputed value is close to the original mean
        expected_mean = self.sample_data['A'].mean()
        # Find index where original was NaN
        nan_index = self.sample_data[self.sample_data['A'].isnull()].index[0]
        self.assertAlmostEqual(df.loc[nan_index, 'A'], expected_mean)
        # Check that non-numeric column 'all_nan' wasn't affected if not specified
        self.assertTrue(df['all_nan'].isnull().all())


    def test_clean_missing_values_median(self):
        resp = self._post_ops([{
            'type': 'missing_values',
            'method': 'median',
            'columns': ['A']
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertIsNotNone(df)
        self.assertFalse(df['A'].isnull().any())
        expected_median = self.sample_data['A'].median()
        nan_index = self.sample_data[self.sample_data['A'].isnull()].index[0]
        self.assertAlmostEqual(df.loc[nan_index, 'A'], expected_median)

    def test_clean_missing_values_mode(self):
        resp = self._post_ops([{
            'type': 'missing_values',
            'method': 'mode',
            'columns': ['B'] # Apply only to column B
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertIsNotNone(df)
        self.assertFalse(df['B'].isnull().any())
        # Original mode of B is 'b' or 'e'. Processor uses first mode ('b').
        nan_index = self.sample_data[self.sample_data['B'].isnull()].index[0]
        self.assertEqual(df.loc[nan_index, 'B'], 'b') # Check the imputed value
        self.assertTrue((df['B'] == 'b').sum() >= 2) # Ensure 'b' count increased or stayed same

    def test_replace_missing_value_constant(self):
        resp = self._post_ops([{
            'type': 'missing_values',
            'method': 'constant',
            'value': '__MISSING__',
            'columns': ['B', 'date'] # Apply to multiple columns
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertIsNotNone(df)
        self.assertFalse(df['B'].isnull().any())
        self.assertFalse(df['date'].isnull().any())
        self.assertIn('__MISSING__', df['B'].unique())
        self.assertIn('__MISSING__', df['date'].unique())
        # Ensure column 'A' is untouched
        self.assertTrue(df['A'].isnull().any())

    def test_remove_missing_data_rows(self):
        # Test removing rows with any NaN in specific columns ('A', 'B')
        resp = self._post_ops([{
            'type': 'missing_values',
            'method': 'remove', # Use remove method
            'how': 'any',        # Specify how ('any' or 'all')
            'columns': ['A', 'B'] # Specify subset of columns to check
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertIsNotNone(df)
        # Check that rows with NaN in A or B were removed
        self.assertFalse(df[['A', 'B']].isnull().any().any())
        # Original had NaNs at index 2 (A) and 3 (B). Both rows should be gone.
        self.assertNotIn(2, df.index)
        self.assertNotIn(3, df.index)
        # Row 4 had NaN in 'date' but not A or B, should still exist
        self.assertIn(4, df.index)


    def test_remove_duplicates(self):
        # Test with specific columns
        resp = self._post_ops([{
            'type': 'remove_duplicates',
            'columns': ['A', 'C'] # Check duplicates based on A and C
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertIsNotNone(df)
        # Original index 4 (A=4.0, C=4.4) is a duplicate of index 3 (A=4.0, C=4.4)
        # (after NaN in A is handled). Let's apply to original data for comparison.
        # Need to be careful if other ops ran before. Use original data.
        expected_df = self.sample_data.drop_duplicates(subset=['A','C'], keep='first')
        self.assertEqual(len(df), len(expected_df))
        # Check indices remaining match expected
        pd.testing.assert_index_equal(df.index, expected_df.index)

    def test_detect_outliers(self):
        # Detect outliers in column C using std dev
        resp = self._post_ops([{
            'type': 'detect_outliers',
            'method': 'std',
            'n_std': 2,          # Use n_std=2 to make 1000.0 an outlier
            'columns': ['C']
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertIsNotNone(df)
        # --- FIX: Check for the standardized column name ---
        self.assertIn('_is_outlier', df.columns)
        # Check that the last value (1000.0) is marked as an outlier
        self.assertTrue(df['_is_outlier'].iloc[-1])
        # Check that other values are not outliers (might depend on exact std calculation)
        mean_c = self.sample_data['C'].mean()
        std_c = self.sample_data['C'].std()
        threshold = mean_c + 2 * std_c
        self.assertFalse(df['_is_outlier'].iloc[0]) # 1.1 should not be outlier
        self.assertFalse(df['_is_outlier'].iloc[1]) # 2.2 should not be outlier
        self.assertGreater(self.sample_data['C'].iloc[-1], threshold) # Verify 1000 is outlier

    def test_replace_outliers(self):
        # Replace outliers in C (detected by std) with the mean
        resp = self._post_ops([{
            'type': 'replace_outliers',
            'method': 'std',       # Detection method
            'n_std': 2,            # Detection threshold
            'replace_with': 'mean', # Replacement method
            'columns': ['C']
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertIsNotNone(df)
        # Calculate mean of non-outliers in C (excluding 1000.0)
        non_outliers = self.sample_data.loc[self.sample_data['C'] < 1000.0, 'C']
        expected_mean = non_outliers.mean()
        # Find index of the outlier (last row in this case)
        outlier_index = self.sample_data[self.sample_data['C'] == 1000.0].index[0]
        # Check if the value at the outlier index is now the mean
        self.assertAlmostEqual(df.loc[outlier_index, 'C'], expected_mean)
        # Ensure other values in C were not changed significantly
        pd.testing.assert_series_equal(df.loc[df.index != outlier_index, 'C'],
                                       self.sample_data.loc[self.sample_data.index != outlier_index, 'C'],
                                       check_names=False)
        # Ensure the temporary _is_outlier column is gone
        self.assertNotIn('_is_outlier', df.columns)


    def test_standardize_format(self):
        resp = self._post_ops([{
             # --- FIX: Use 'type' not 'operation_type' ---
            'type': 'standardize_format',
            'date_columns': ['date'],
            'number_columns': ['A','C']
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertIsNotNone(df)
        # Check date column type and NaT for invalid date
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['date']))
        # Find index where original was 'notadate'
        invalid_date_index = self.sample_data[self.sample_data['date'] == 'notadate'].index[0]
        self.assertTrue(pd.isna(df.loc[invalid_date_index, 'date'])) # Should be NaT
        # Check numeric column types
        self.assertTrue(pd.api.types.is_numeric_dtype(df['A']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['C']))


    def test_cluster_similar_values(self):
        # This is currently a no-op stub
        resp = self._post_ops([{
            'type': 'cluster_similar',
            'column': 'B',
            'threshold': 0.5 # Example param, ignored by stub
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertIsNotNone(df)
        # Check that the DataFrame is unchanged by the stub
        pd.testing.assert_frame_equal(df, self.sample_data, check_dtype=False) # Allow type changes from load/save cycle


    def test_multiple_operations(self):
        # Define a sequence of operations
        ops = [
            {'type': 'missing_values', 'method': 'mean', 'columns': ['A']}, # Fill NaN in A
            {'type': 'remove_duplicates', 'columns': ['A','C']},            # Remove duplicate row based on A, C
            # Detect outliers in C (1000.0) - adds _is_outlier
            {'type': 'detect_outliers',   'method': 'std', 'n_std': 2, 'columns': ['C']},
             # Replace outliers in C (1000.0) with median of non-outliers
            {'type': 'replace_outliers',  'method': 'std', 'n_std': 2, 'replace_with': 'median', 'columns': ['C']}
        ]
        resp = self._post_ops(ops)
        self.assertEqual(resp.status_code, 200, resp.content) # Print content on failure
        df = self._reload()
        self.assertIsNotNone(df)

        # Verify results:
        # 1. NaN in A should be filled
        self.assertFalse(df['A'].isnull().any())

        # 2. Duplicates based on A, C removed (row 4 removed)
        # Original A,C pairs: (1,1.1), (2,2.2), (NaN,3.3), (4,4.4), (4,4.4), (100,1000)
        # After A filled: (1,1.1), (2,2.2), (~4.1,3.3), (4,4.4), (4,4.4), (100,1000)
        # Expected remaining indices (keep='first'): 0, 1, 2, 3, 5
        self.assertNotIn(4, df.index)
        self.assertIn(3, df.index)

        # 3. Outlier in C (originally 1000.0 at index 5) replaced with median
        # Calculate median of C for non-outliers *before* duplicate removal
        # Outlier detection uses n_std=2, identifies 1000.0
        non_outliers_original = self.sample_data.loc[self.sample_data['C'] < 1000, 'C']
        expected_median = non_outliers_original.median() # Median of [1.1, 2.2, 3.3, 4.4, 4.4] -> 3.3

        # Check value at original index 5 in the final df
        self.assertAlmostEqual(df.loc[5, 'C'], expected_median)

        # 4. _is_outlier column should be gone (removed by replace_outliers)
        self.assertNotIn('_is_outlier', df.columns)


    def test_invalid_operation_type(self):
        resp = self._post_ops([{'type': 'does_not_exist'}])
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.json())
        self.assertIn("No data-cleaner processor found", resp.json()['error'])

    def test_invalid_operation_params(self):
        # Missing 'method' for missing_values
        resp = self._post_ops([{'type': 'missing_values', 'columns': ['A']}])
        self.assertEqual(resp.status_code, 400) # Expecting error due to missing param
        self.assertIn('error', resp.json())
        self.assertIn("Invalid parameters", resp.json()['error'])
        self.assertIn("Missing 'method' parameter", resp.json()['details'])

        # Missing 'value' for missing_values constant method
        resp = self._post_ops([{'type': 'missing_values', 'method': 'constant', 'columns': ['A']}])
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.json())
        self.assertIn("'constant' replacement requires a 'value' parameter", resp.json()['details'])


    def test_nonexistent_dataset(self):
        # Remove the file before making the request
        os.remove(self.active_parquet_path)
        resp = self._post_ops([{
            'type':'missing_values',
            'method':'mean',
            'columns':['A']
        }])
        # View should return 404 if get_active_dataset returns None or raises FileNotFoundError
        self.assertEqual(resp.status_code, 404)
        self.assertIn('error', resp.json())
        self.assertIn("not found", resp.json()['error'].lower()) # Check for variations


    def test_available_cleaning_tools(self):
        resp = self.client.get(reverse('datacleaning:available-cleaning-tools'))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('cleaning_tools', data)
        tools = data['cleaning_tools']
        # --- FIX: Check for the actual keys registered in the factory ---
        expected_tools = [
            'missing_values', 'remove_duplicates', 'detect_outliers',
            'replace_outliers', 'standardize_format', 'cluster_similar'
        ]
        self.assertListEqual(sorted(tools), sorted(expected_tools))


    # --- FIX: Rewrite test to check a specific processor instance ---
    def test_processor_instance_directly(self):
        # Test RemoveDuplicatesCleaner directly
        processor = RemoveDuplicatesCleaner()
        params = {'columns': ['B']} # Remove duplicates based on column B
        # Create df with duplicates in B: ['a', 'b', 'b', None, 'e', 'e']
        # Expected: keep first 'b' (idx 1), first 'e' (idx 4)
        df_in = self.sample_data.copy()
        df_out = processor.apply(df_in, **params)

        # Expected indices remaining (keep='first'): 0, 1, 3, 4
        expected_indices = pd.Index([0, 1, 3, 4])
        pd.testing.assert_index_equal(df_out.index, expected_indices)

        # Test MissingValuesCleaner directly
        processor_mv = MissingValuesCleaner()
        params_mv = {'method': 'constant', 'value': -99, 'columns': ['A']}
        df_out_mv = processor_mv.apply(df_in.copy(), **params_mv) # Use copy
        nan_index_A = df_in[df_in['A'].isnull()].index[0]
        self.assertEqual(df_out_mv.loc[nan_index_A, 'A'], -99)
        self.assertFalse(df_out_mv['A'].isnull().any()) # Check if all NaNs in A are filled
        # Ensure other NaNs (e.g., in B) are untouched
        self.assertTrue(df_out_mv['B'].isnull().any())