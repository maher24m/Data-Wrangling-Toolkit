from django.test import TestCase, Client
from django.urls import reverse
from api.storage import save_dataset, delete_dataset
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
        self.assertIn('data', data)
        self.assertEqual(len(data['data']), 3) 

    def test_get_nonexistent_dataset(self):
        """Test retrieving a dataset that doesn't exist"""
        response = self.client.get(reverse('datasets:dataset-detail', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_dataset_manager_save(self):
        """Test saving a dataset"""
        from api.datasets.manager import DatasetManager
        test_data = pd.DataFrame({'test': [1, 2, 3]})
        file_path = DatasetManager.save_dataset('test_save', test_data)
        self.assertTrue(os.path.exists(file_path))
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_dataset_manager_get(self):
        """Test retrieving a dataset through the manager"""
        from api.datasets.manager import DatasetManager
        test_data = pd.DataFrame({'test': [1, 2, 3]})
        file_path = DatasetManager.save_dataset('test_get', test_data)
        retrieved_data = DatasetManager.get_dataset('test_get')
        self.assertIsNotNone(retrieved_data)
        self.assertEqual(len(retrieved_data), 3)
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_active_dataset(self):
        """Test setting and getting active dataset"""
        from api.datasets.manager import DatasetManager
        test_data = pd.DataFrame({'test': [1, 2, 3]})
        file_path = DatasetManager.save_dataset('test_active', test_data)
        DatasetManager.set_active_dataset('test_active')
        active_data = DatasetManager.get_active_dataset()
        self.assertIsNotNone(active_data)
        self.assertEqual(len(active_data), 3)
        if os.path.exists(file_path):
            os.remove(file_path)
