from django.test import TestCase, Client
from django.urls import reverse
from api.datasets.manager import save_dataset
from api.export_app.exporters import Exporter
import pandas as pd
import json
import os

class ExportAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a sample dataset for testing
        self.sample_data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['a', 'b', 'c']
        })
        self.dataset_name = 'test_export'
        save_dataset(self.dataset_name, self.sample_data)

    def tearDown(self):
        # Clean up test files
        if os.path.exists('exports/test_export.csv'):
            os.remove('exports/test_export.csv')
        if os.path.exists('exports/test_export.json'):
            os.remove('exports/test_export.json')
        if os.path.exists('exports/test_export.xml'):
            os.remove('exports/test_export.xml')

    def test_export_csv(self): # failure
        """Test exporting to CSV format"""
        response = self.client.post(
            reverse('export_app:file_export'),
            {
                'dataset_name': self.dataset_name,
                'file_type': 'csv'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'csv')
        self.assertTrue(os.path.exists('exports/test_export.csv'))

    def test_export_json(self): 
        """Test exporting to JSON format"""
        response = self.client.post(
            reverse('export_app:file_export'),
            {
                'dataset_name': self.dataset_name,
                'file_type': 'json'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'json')
        self.assertTrue(os.path.exists('exports/test_export.json'))

    def test_export_xml(self):
        """Test exporting to XML format"""
        response = self.client.post(
            reverse('export_app:file_export'),
            {
                'dataset_name': self.dataset_name,
                'file_type': 'xml'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'xml')
        self.assertTrue(os.path.exists('exports/test_export.xml'))

    def test_export_invalid_format(self):
        """Test exporting with invalid format"""
        response = self.client.post(
            reverse('export_app:file_export'),
            {
                'dataset_name': self.dataset_name,
                'file_type': 'invalid'
            }
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_export_nonexistent_dataset(self): 
        """Test exporting nonexistent dataset"""
        response = self.client.post(
            reverse('export_app:file_export'),
            {
                'dataset_name': 'nonexistent',
                'file_type': 'csv'
            }
        )
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_available_export_tools(self):
        """Test getting available export tools"""
        response = self.client.get(reverse('export_app:available_export_tools'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('export_tools', data)
        self.assertIsInstance(data['export_tools'], list)
        self.assertIn('csv', data['export_tools'])
        self.assertIn('json', data['export_tools'])
        self.assertIn('xml', data['export_tools'])

    def test_exporter_csv(self):
        """Test CSV exporter"""
        from api.export_app.exporters import Exporter
        exporter = Exporter()
        exporter.export(self.sample_data, 'exports/test_export.csv')
        self.assertTrue(os.path.exists('exports/test_export.csv'))
        df = pd.read_csv('exports/test_export.csv')
        self.assertEqual(len(df), 3)
        self.assertEqual(list(df.columns), ['A', 'B'])

    def test_exporter_json(self): #error
        """Test JSON exporter"""
        from api.export_app.exporters import Exporter
        exporter = Exporter()
        exporter.export(self.sample_data, 'exports/test_export.json')
        self.assertTrue(os.path.exists('exports/test_export.json'))
        df = pd.read_json('exports/test_export.json') #parsing error
        self.assertEqual(len(df), 3)
        self.assertEqual(list(df.columns), ['A', 'B'])
