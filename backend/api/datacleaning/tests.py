# backend/api/datacleaning/tests.py
from django.test import TestCase, Client
from django.urls import reverse
import pandas as pd
import numpy as np
import json
import os

class DataCleaningTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a sample dataset with missing values, duplicates, outliers, and mixed formats
        self.sample_data = pd.DataFrame({
            'A': [1, 2, None, 4, 4, 100],
            'B': ['a', 'b', 'b', None, 'e', 'e'],
            'C': [1.1, 2.2, 3.3, 4.4, 4.4, 1000.0],
            'date': ['2020-01-01', '2020/02/01', 'notadate', None, '2020-03-15', '2020-04-01']
        })
        os.makedirs('datasets', exist_ok=True)
        # Save it under the one and only “active” dataset slot
        self.sample_data.to_parquet('datasets/active.parquet')

    def tearDown(self):
        # Clean up test file
        try:
            os.remove('datasets/active.parquet')
        except OSError:
            pass

    def _post_ops(self, ops):
        return self.client.post(
            reverse('datacleaning:data-cleaning'),
            {'operations': json.dumps(ops)},
            content_type='application/json'
        )

    def _reload(self):
        return pd.read_parquet('datasets/active.parquet')

    def test_clean_missing_values_mean(self):
        resp = self._post_ops([{
            'type': 'missing_values',
            'method': 'mean',
            'columns': ['A']
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertFalse(df['A'].isnull().any())

    def test_clean_missing_values_median(self):
        resp = self._post_ops([{
            'type': 'missing_values',
            'method': 'median',
            'columns': ['A']
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertFalse(df['A'].isnull().any())
        expected = self.sample_data['A'].median(skipna=True)
        self.assertAlmostEqual(df.loc[2, 'A'], expected)

    def test_clean_missing_values_mode(self):
        resp = self._post_ops([{
            'type': 'missing_values',
            'method': 'mode',
            'columns': ['B']
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertFalse(df['B'].isnull().any())
        self.assertTrue((df['B'] == 'b').sum() >= 2)

    def test_replace_missing_value(self):
        resp = self._post_ops([{
            'type': 'missing_values',
            'method': 'constant',
            'value': '__MISSING__',
            'columns': ['B', 'date']
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertNotIn(None, df['B'].values)
        self.assertIn('__MISSING__', df['date'].values)

    def test_remove_missing_data(self):
        resp = self._post_ops([{
            'type': 'remove_missing',
            'how': 'any'
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertFalse(df.isnull().any().any())

    def test_remove_duplicates(self):
        resp = self._post_ops([{
            'type': 'remove_duplicates',
            'columns': ['A', 'C']
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertEqual(len(df), len(self.sample_data.drop_duplicates(subset=['A','C'])))

    def test_detect_outliers(self):
        resp = self._post_ops([{
            'type': 'detect_outliers',
            'method': 'std',
            'n_std': 2,
            'columns': ['C']
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertIn('_is_outlier_C', df.columns)
        self.assertTrue(df['_is_outlier_C'].iloc[-1])

    def test_replace_outliers(self):
        resp = self._post_ops([{
            'type': 'replace_outliers',
            'method': 'std',
            'n_std': 2,
            'replace_with': 'mean',
            'columns': ['C']
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        mean_c = self.sample_data['C'].mean(skipna=True)
        self.assertAlmostEqual(df.loc[df.index[-1], 'C'], mean_c)

    def test_standardize_format(self):
        resp = self._post_ops([{
            'operation_type': 'standardize_format',
            'date_columns': ['date'],
            'number_columns': ['A','C']
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['date']))
        self.assertTrue(pd.isna(df.loc[2, 'date']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['A']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['C']))

    def test_cluster_similar_values(self):
        resp = self._post_ops([{
            'type': 'cluster_similar',
            'column': 'B',
            'threshold': 0.5
        }])
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        pd.testing.assert_frame_equal(df, self.sample_data, check_dtype=False)

    def test_multiple_operations(self):
        ops = [
            {'type': 'missing_values', 'method': 'mean', 'columns': ['A']},
            {'type': 'remove_duplicates', 'columns': ['A','C']},
            {'type': 'detect_outliers',   'method': 'std', 'n_std': 2, 'columns': ['C']},
            {'type': 'replace_outliers',  'method': 'std', 'n_std': 2, 'replace_with': 'median', 'columns': ['C']}
        ]
        resp = self._post_ops(ops)
        self.assertEqual(resp.status_code, 200)
        df = self._reload()
        self.assertFalse(df['A'].isnull().any())
        self.assertEqual(len(df), len(self.sample_data.drop_duplicates(subset=['A','C'])))
        self.assertLess(df['C'].max(), self.sample_data['C'].max())

    def test_invalid_operation(self):
        resp = self._post_ops([{'type': 'does_not_exist'}])
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.json())

    def test_nonexistent_dataset(self):
        # Since there's no URL-arg for dataset_name anymore,
        # we just clear out the active.parquet
        os.remove('datasets/active.parquet')
        resp = self.client.post(
            reverse('datacleaning:data-cleaning'),
            {'operations': json.dumps([{
                'type':'missing_values',
                'method':'mean',
                'columns':['A']
            }])},
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 404)
        self.assertIn('error', resp.json())

    def test_available_cleaning_tools(self):
        resp = self.client.get(reverse('datacleaning:available-cleaning-tools'))
        self.assertEqual(resp.status_code, 200)
        tools = resp.json()['cleaning_tools']
        for op in [
            'missing_values','remove_missing','remove_duplicates',
            'detect_outliers','replace_outliers','standardize_format','cluster_similar'
        ]:
            self.assertIn(op, tools)

    def test_cleaning_processor_directly(self):
        from api.datacleaning.processor import DataCleaningFactory
        proc = DataCleaningFactory()
        out = proc.apply(self.sample_data.copy())
        self.assertIsInstance(out, pd.DataFrame)
        self.assertFalse(out['A'].isnull().any())
