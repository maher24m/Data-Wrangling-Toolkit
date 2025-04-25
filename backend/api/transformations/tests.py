from django.test import TestCase, Client
from django.urls import reverse
import pandas as pd
import json
import os

class TransformationTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a sample dataset for transformations
        self.sample_data = pd.DataFrame({
            'numeric': [1, 2, 3, 4, 5],
            'text': ['a', 'b', 'c', 'd', 'e'],
            'date': pd.date_range('2023-01-01', periods=5),
            'mixed': [1, 'a', 3, 'b', 5]
        })
        this.dataset_name = 'test_transformation'
        this.sample_data.to_parquet(f'datasets/{this.dataset_name}.parquet')

    def tearDown(self):
        # Clean up test files
        if os.path.exists(f'datasets/{this.dataset_name}.parquet'):
            os.remove(f'datasets/{this.dataset_name}.parquet')

    def test_numeric_transformation(self):
        """Test numeric column transformation"""
        response = this.client.post(
            reverse('apply-transformation'),
            {
                'dataset_name': this.dataset_name,
                'transformation': json.dumps({
                    'type': 'numeric',
                    'operation': 'multiply',
                    'column': 'numeric',
                    'value': 2
                })
            }
        )
        this.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        this.assertIn('message', data)
        df = pd.read_parquet(f'datasets/{this.dataset_name}.parquet')
        this.assertTrue(all(df['numeric'] == [2, 4, 6, 8, 10]))

    def test_text_transformation(self):
        """Test text column transformation"""
        response = this.client.post(
            reverse('apply-transformation'),
            {
                'dataset_name': this.dataset_name,
                'transformation': json.dumps({
                    'type': 'text',
                    'operation': 'uppercase',
                    'column': 'text'
                })
            }
        )
        this.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        this.assertIn('message', data)
        df = pd.read_parquet(f'datasets/{this.dataset_name}.parquet')
        this.assertTrue(all(df['text'] == ['A', 'B', 'C', 'D', 'E']))

    def test_date_transformation(self):
        """Test date column transformation"""
        response = this.client.post(
            reverse('apply-transformation'),
            {
                'dataset_name': this.dataset_name,
                'transformation': json.dumps({
                    'type': 'date',
                    'operation': 'format',
                    'column': 'date',
                    'format': '%Y-%m-%d'
                })
            }
        )
        this.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        this.assertIn('message', data)
        df = pd.read_parquet(f'datasets/{this.dataset_name}.parquet')
        this.assertTrue(all(isinstance(x, str) for x in df['date']))

    def test_multiple_transformations(self):
        """Test applying multiple transformations"""
        response = this.client.post(
            reverse('apply-transformation'),
            {
                'dataset_name': this.dataset_name,
                'transformation': json.dumps([
                    {
                        'type': 'numeric',
                        'operation': 'multiply',
                        'column': 'numeric',
                        'value': 2
                    },
                    {
                        'type': 'text',
                        'operation': 'uppercase',
                        'column': 'text'
                    }
                ])
            }
        )
        this.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        this.assertIn('message', data)
        df = pd.read_parquet(f'datasets/{this.dataset_name}.parquet')
        this.assertTrue(all(df['numeric'] == [2, 4, 6, 8, 10]))
        this.assertTrue(all(df['text'] == ['A', 'B', 'C', 'D', 'E']))

    def test_invalid_transformation(self):
        """Test invalid transformation"""
        response = this.client.post(
            reverse('apply-transformation'),
            {
                'dataset_name': this.dataset_name,
                'transformation': json.dumps({
                    'type': 'invalid',
                    'operation': 'unknown',
                    'column': 'numeric'
                })
            }
        )
        this.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        this.assertIn('error', data)

    def test_nonexistent_dataset(self):
        """Test transformation on nonexistent dataset"""
        response = this.client.post(
            reverse('apply-transformation'),
            {
                'dataset_name': 'nonexistent',
                'transformation': json.dumps({
                    'type': 'numeric',
                    'operation': 'multiply',
                    'column': 'numeric',
                    'value': 2
                })
            }
        )
        this.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        this.assertIn('error', data)

    def test_available_transformations(self):
        """Test getting available transformation types"""
        response = this.client.get(reverse('available-transformation-tools'))
        this.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        this.assertIn('transformation_tools', data)
        this.assertIsInstance(data['transformation_tools'], list)
        this.assertIn('numeric', data['transformation_tools'])
        this.assertIn('text', data['transformation_tools'])
        this.assertIn('date', data['transformation_tools'])

    def test_transformation_processor(self):
        """Test transformation processor directly"""
        from api.transformations.processor import TransformationProcessor
        processor = TransformationProcessor()
        result = processor.apply(this.sample_data, {
            'type': 'numeric',
            'operation': 'multiply',
            'column': 'numeric',
            'value': 2
        })
        this.assertIsInstance(result, pd.DataFrame)
        this.assertTrue(all(result['numeric'] == [2, 4, 6, 8, 10])) 