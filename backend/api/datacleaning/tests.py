from django.test import TestCase, Client
from django.urls import reverse
import pandas as pd
import json
import os

class DataCleaningTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a sample dataset with missing values and duplicates
        self.sample_data = pd.DataFrame({
            'A': [1, 2, None, 4, 4],
            'B': ['a', 'b', 'c', None, 'e'],
            'C': [1.1, 2.2, 3.3, 4.4, 4.4]
        })
        self.dataset_name = 'test_cleaning'
        self.sample_data.to_parquet(f'datasets/{self.dataset_name}.parquet')

    def tearDown(self):
        # Clean up test files
        if os.path.exists(f'datasets/{self.dataset_name}.parquet'):
            os.remove(f'datasets/{self.dataset_name}.parquet')

    def test_clean_missing_values(self):
        """Test cleaning missing values"""
        response = self.client.post(
            reverse('data-cleaning', args=[self.dataset_name]),
            {
                'operations': json.dumps([{
                    'type': 'missing_values',
                    'method': 'mean',
                    'columns': ['A']
                }])
            }
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        df = pd.read_parquet(f'datasets/{self.dataset_name}.parquet')
        self.assertFalse(df['A'].isnull().any())

    def test_remove_duplicates(self):
        """Test removing duplicate rows"""
        response = self.client.post(
            reverse('data-cleaning', args=[self.dataset_name]),
            {
                'operations': json.dumps([{
                    'type': 'remove_duplicates',
                    'columns': ['A', 'C']
                }])
            }
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        df = pd.read_parquet(f'datasets/{self.dataset_name}.parquet')
        self.assertEqual(len(df), 4)  # One duplicate row should be removed

    def test_multiple_operations(self):
        """Test applying multiple cleaning operations"""
        response = self.client.post(
            reverse('data-cleaning', args=[self.dataset_name]),
            {
                'operations': json.dumps([
                    {
                        'type': 'missing_values',
                        'method': 'mean',
                        'columns': ['A']
                    },
                    {
                        'type': 'remove_duplicates',
                        'columns': ['A', 'C']
                    }
                ])
            }
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        df = pd.read_parquet(f'datasets/{self.dataset_name}.parquet')
        self.assertFalse(df['A'].isnull().any())
        self.assertEqual(len(df), 4)

    def test_invalid_operation(self):
        """Test invalid cleaning operation"""
        response = self.client.post(
            reverse('data-cleaning', args=[self.dataset_name]),
            {
                'operations': json.dumps([{
                    'type': 'invalid_operation',
                    'method': 'mean',
                    'columns': ['A']
                }])
            }
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_nonexistent_dataset(self):
        """Test cleaning nonexistent dataset"""
        response = self.client.post(
            reverse('data-cleaning', args=['nonexistent']),
            {
                'operations': json.dumps([{
                    'type': 'missing_values',
                    'method': 'mean',
                    'columns': ['A']
                }])
            }
        )
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_available_cleaning_tools(self):
        """Test getting available cleaning tools"""
        response = self.client.get(reverse('available-cleaning-tools'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('cleaning_tools', data)
        self.assertIsInstance(data['cleaning_tools'], list)
        self.assertIn('missing_values', data['cleaning_tools'])
        self.assertIn('remove_duplicates', data['cleaning_tools'])

    def test_cleaning_processor(self):
        """Test cleaning processor directly"""
        from api.datacleaning.processor import CleaningProcessor
        processor = CleaningProcessor()
        df = processor.apply(self.sample_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 5)  # Original length
        self.assertFalse(df['A'].isnull().any())  # No missing values
