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

        self.parquet_content = b"col1,col2\n1,a\n2,b\n3,c"
        self.parquet_file = SimpleUploadedFile("test.parquet", self.parquet_content, content_type="application/octet-stream")

        self.xml_content = b"<root><item><col1>1</col1><col2>a</col2></item><item><col1>2</col1><col2>b</col2></item></root>"
        self.xml_file = SimpleUploadedFile("test.xml", self.xml_content, content_type="application/xml")

        self.excel_content = b"col1,col2\n1,a\n2,b\n3,c"
        self.excel_file = SimpleUploadedFile("test.xlsx", self.excel_content, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

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
            {'file': self.csv_file, 'dataset_name': 'csv'},
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
            {'file': self.json_file,'dataset_name': 'json'},
            format='multipart'
        )
        self.assertEqual(response.status_code, 200) 
        data = json.loads(response.content)
        self.assertIn('success', data)
        self.assertTrue(os.path.exists(f'stored_datasets/{data["dataset_name"]}.parquet'))

    def test_file_upload_xml(self):
        """Test uploading an XML file"""

        response = self.client.post(
            reverse('import_app:file-upload'),
            {'file': self.xml_file, 'dataset_name': 'test_xml'},
            format='multipart'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('success', data)
        self.assertTrue(os.path.exists(f'stored_datasets/{data["dataset_name"]}.parquet'))

    def test_file_upload_parquet(self): #Works but test fails
        """Test uploading a Parquet file"""
        
        response = self.client.post(
            reverse('import_app:file-upload'),
            {'file': self.parquet_file, 'dataset_name': 'test_parquet'},
            format='multipart'
        )
        print(response.content)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('success', data)
        self.assertTrue(os.path.exists(f'stored_datasets/{data["dataset_name"]}.parquet'))

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
        print(response.content)
        data = json.loads(response.content)
        self.assertIn('import_tools', data)
        self.assertIsInstance(data['import_tools'], list)
        self.assertIn('text/csv', data['import_tools'])
        self.assertIn('application/json', data['import_tools'])


