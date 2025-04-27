from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import pandas as pd
import json
import os

class ImportAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create sample files for testing
        self.csv_content = b"col1,col2\n1,a\n2,b\n3,c"
        self.csv_file = SimpleUploadedFile("test.csv", self.csv_content, content_type="text/csv")
        
        self.json_content = b'[{"col1": 1, "col2": "a"}, {"col1": 2, "col2": "b"}]'
        self.json_file = SimpleUploadedFile("test.json", self.json_content, content_type="application/json")

    def tearDown(self):
        # Clean up any created files
        if os.path.exists('datasets/test.csv'):
            os.remove('datasets/test.csv')
        if os.path.exists('datasets/test.json'):
            os.remove('datasets/test.json')

    def test_file_upload_csv(self):
        """Test uploading a CSV file"""
        response = self.client.post(
            reverse('import_app:file-upload'), 
            {'file': self.csv_file, 'dataset_name': 'pep'},
            format='multipart'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('success', data)
        self.assertTrue(os.path.exists(f'stored_datasets/{data["dataset_name"]}.parquet'))

    def test_file_upload_json(self):
        """Test uploading a JSON file"""
        response = self.client.post(
            reverse('import_app:file-upload'),
            {'file': self.json_file,'file_type': 'json'},
            format='multipart'
        )
        self.assertEqual(response.status_code, 200) #400 != 200
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertTrue(os.path.exists(f'datasets/{data["dataset_name"]}.parquet'))

    def test_file_upload_invalid_type(self):
        """Test uploading a file with invalid type"""
        response = self.client.post(
            reverse('import_app:file-upload'),
            {'file': self.csv_file, 'file_type': 'invalid'},
            format='multipart'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_file_upload_no_file(self):
        """Test uploading without a file"""
        response = self.client.post(
            reverse('import_app:file-upload'),
            {'file_type': 'csv'},
            format='multipart'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_available_import_tools(self):
        """Test getting available import tools"""
        response = self.client.get(reverse('import_app:available-import-tools')) 
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('import_tools', data)
        self.assertIsInstance(data['import_tools'], list)
        self.assertIn('csv', data['import_tools'])
        self.assertIn('json', data['import_tools'])

    def test_file_processor_csv(self): 
        """Test CSV file processor"""
        from api.import_app.processors import FileProcessor
        processor = FileProcessor()
        df = processor.process(self.csv_file)
        self.assertIsInstance(df, pd.DataFrame) 
        self.assertEqual(len(df), 3)
        self.assertEqual(list(df.columns), ['col1', 'col2'])

    def test_file_processor_json(self): 
        """Test JSON file processor"""
        from api.import_app.processors import FileProcessor
        processor = FileProcessor()
        df = processor.process(self.json_file)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ['col1', 'col2'])
