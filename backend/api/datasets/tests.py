from django.test import TestCase, Client
from django.urls import reverse
from api.datasets.manager import save_dataset, delete_dataset, get_dataset
import pandas as pd
import os
import json

class DatasetTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a sample dataset for testing
        self.sample_data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['a', 'b', 'c']
        })
        self.dataset_name = 'test_dataset'
        save_dataset(self.dataset_name, self.sample_data.to_dict(orient="records"))

    def tearDown(self):
        # Clean up test files
        delete_dataset(self.dataset_name)

    def test_list_datasets(self):
        """Test listing available datasets"""
        response = self.client.get(reverse("datasets:dataset-list"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('datasets', data)
        self.assertIsInstance(data['datasets'], list)

    def test_get_dataset(self):
        """Test retrieving a specific dataset"""
        response = self.client.get(reverse('datasets:dataset-detail', args=[self.dataset_name]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('values', data)
        self.assertEqual(len(data['values']), 3)

    def test_get_dataset_columns(self):
        """Test retrieving dataset columns"""
        response = self.client.get(reverse('datasets:dataset-columns', args=[self.dataset_name]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('columns', data)
        self.assertEqual(data['columns'], ['A', 'B'])

    def test_get_nonexistent_dataset(self):
        """Test retrieving a dataset that doesn't exist"""
        response = self.client.get(reverse('datasets:dataset-detail', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_get_nonexistent_dataset_columns(self):
        """Test retrieving columns for a dataset that doesn't exist"""
        response = self.client.get(reverse('datasets:dataset-columns', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_dataset_manager_save(self):
        """Test saving a dataset"""
        test_data = pd.DataFrame({'test': [1, 2, 3]})
        file_path = save_dataset('test_save', test_data)
        self.assertTrue(os.path.exists(file_path))
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_dataset_manager_get(self):
        """Test retrieving a dataset through the manager"""
        test_data = pd.DataFrame({'test': [1, 2, 3]})
        file_path = save_dataset('test_get', test_data)
        retrieved_data = get_dataset('test_get')
        self.assertIsNotNone(retrieved_data)
        print(len(retrieved_data))
        self.assertEqual(len(retrieved_data), 3)
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_save_dataset(self):
        """Test saving updates to a dataset"""
        # Prepare updated data
        updated_data = {
            'data': [
                {'A': 4, 'B': 'd'},
                {'A': 5, 'B': 'e'},
                {'A': 6, 'B': 'f'}
            ]
        }

        # Make POST request to save endpoint
        response = self.client.post(
            reverse('datasets:dataset-save', args=[self.dataset_name]),
            data=json.dumps(updated_data),
            content_type='application/json'
        )

        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertIn('data', data)
        self.assertEqual(len(data['data']), 3)

        # Verify the data was actually saved
        saved_dataset = get_dataset(self.dataset_name)
        self.assertEqual(len(saved_dataset), 3)
        self.assertEqual(saved_dataset.iloc[0]['A'], 4)
        self.assertEqual(saved_dataset.iloc[0]['B'], 'd')

    def test_save_dataset_invalid_json(self):
        """Test saving dataset with invalid JSON"""
        response = self.client.post(
            reverse('datasets:dataset-save', args=[self.dataset_name]),
            data='invalid json',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_save_dataset_missing_data(self):
        """Test saving dataset with missing data field"""
        invalid_data = {
            'wrong_field': [
                {'A': 4, 'B': 'd'}
            ]
        }

        response = self.client.post(
            reverse('datasets:dataset-save', args=[self.dataset_name]),
            data=json.dumps(invalid_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_save_nonexistent_dataset(self):
        """Test saving to a dataset that doesn't exist"""
        updated_data = {
            'data': [
                {'A': 4, 'B': 'd'}
            ]
        }

        response = self.client.post(
            reverse('datasets:dataset-save', args=['nonexistent_dataset']),
            data=json.dumps(updated_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_save_dataset_empty_data(self):
        """Test saving dataset with empty data"""
        empty_data = {
            'data': []
        }

        response = self.client.post(
            reverse('datasets:dataset-save', args=[self.dataset_name]),
            data=json.dumps(empty_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        
        # Verify the dataset is now empty
        saved_dataset = get_dataset(self.dataset_name)
        self.assertEqual(len(saved_dataset), 0)