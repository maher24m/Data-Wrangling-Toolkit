from django.test import TestCase, Client
from django.urls import reverse
import pandas as pd
import numpy as np
import json
import os
from .factory import TransformationFactory
from .processor import (
    BaseTransformationProcessor,
    NormalizeProcessor,
    LogProcessor,
    SquareRootProcessor
)
from api.datasets.manager import save_dataset, delete_dataset, get_dataset

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
        self.dataset_name = 'test_transformation'
        self.sample_data.to_parquet(f'datasets/{self.dataset_name}.parquet')

    def tearDown(self):
        # Clean up test files
        if os.path.exists(f'datasets/{self.dataset_name}.parquet'):
            os.remove(f'datasets/{self.dataset_name}.parquet')

    def test_numeric_transformation(self):
        """Test numeric column transformation"""
        response = self.client.post(
            reverse('transformations:apply-transformation', args=[self.dataset_name]),
            data=json.dumps({
                'transformation': 'NormalizeProcessor',
                'parameters': {
                    'column': 'numeric'
                }
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        df = pd.read_parquet(f'datasets/{self.dataset_name}.parquet')
        self.assertTrue(all(df['numeric'] == [2, 4, 6, 8, 10]))

    def test_text_transformation(self):
        """Test text column transformation"""
        response = self.client.post(
            reverse('transformations:apply-transformation', args=[self.dataset_name]),
            data=json.dumps({
                'transformation': 'LogProcessor',
                'parameters': {
                    'column': 'text'
                }
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        df = pd.read_parquet(f'datasets/{self.dataset_name}.parquet')
        self.assertTrue(all(df['text'] == ['A', 'B', 'C', 'D', 'E']))

    def test_date_transformation(self):
        """Test date column transformation"""
        response = self.client.post(
            reverse('transformations:apply-transformation', args=[self.dataset_name]),
            data=json.dumps({
                'transformation': 'SquareRootProcessor',
                'parameters': {
                    'column': 'date'
                }
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        df = pd.read_parquet(f'datasets/{self.dataset_name}.parquet')
        this.assertTrue(all(isinstance(x, str) for x in df['date']))

    def test_multiple_transformations(self):
        """Test applying multiple transformations"""
        response = self.client.post(
            reverse('transformations:apply-transformation', args=[self.dataset_name]),
            data=json.dumps({
                'transformation': 'NormalizeProcessor',
                'parameters': {
                    'column': 'numeric'
                }
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        this.assertIn('message', data)
        df = pd.read_parquet(f'datasets/{self.dataset_name}.parquet')
        this.assertTrue(all(df['numeric'] == [2, 4, 6, 8, 10]))

    def test_invalid_transformation(self):
        """Test invalid transformation"""
        response = self.client.post(
            reverse('transformations:apply-transformation', args=[self.dataset_name]),
            data=json.dumps({
                'transformation': 'InvalidProcessor',
                'parameters': {
                    'column': 'numeric'
                }
            }),
            content_type='application/json'
        )
        this.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        this.assertIn('error', data)

    def test_nonexistent_dataset(self):
        """Test transformation on nonexistent dataset"""
        response = self.client.post(
            reverse('transformations:apply-transformation', args=['nonexistent']),
            data=json.dumps({
                'transformation': 'NormalizeProcessor',
                'parameters': {
                    'column': 'numeric'
                }
            }),
            content_type='application/json'
        )
        this.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        this.assertIn('error', data)

    def test_available_transformations(self):
        """Test getting available transformation types"""
        response = self.client.get(reverse('transformations:available-transformations'))
        this.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        this.assertIn('transformations', data)
        this.assertIsInstance(data['transformations'], dict)
        this.assertIn('NormalizeProcessor', data['transformations'])
        this.assertIn('LogProcessor', data['transformations'])
        this.assertIn('SquareRootProcessor', data['transformations'])

class TransformationProcessorTests(TestCase):
    """Test cases for transformation processors"""
    
    def setUp(self):
        # Create a sample dataframe for testing
        self.df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50]
        })
        
    def test_normalize_processor(self):
        processor = NormalizeProcessor()
        result = processor.transform(self.df.copy(), column='A')
        
        # Check if values are normalized between 0 and 1
        self.assertTrue(result['A'].min() == 0)
        self.assertTrue(result['A'].max() == 1)
        self.assertEqual(processor.name, "NormalizeProcessor")
        self.assertIn('column', processor.parameters)

    def test_log_processor(self):
        processor = LogProcessor()
        result = processor.transform(self.df.copy(), column='A')
        
        # Check if log transformation was applied
        expected = np.log1p(self.df['A'])
        np.testing.assert_array_almost_equal(result['A'], expected)
        self.assertEqual(processor.name, "LogProcessor")
        self.assertIn('column', processor.parameters)

    def test_square_root_processor(self):
        processor = SquareRootProcessor()
        result = processor.transform(self.df.copy(), column='A')
        
        # Check if square root transformation was applied
        expected = np.sqrt(self.df['A'])
        np.testing.assert_array_almost_equal(result['A'], expected)
        self.assertEqual(processor.name, "SquareRootProcessor")
        self.assertIn('column', processor.parameters)

class TransformationFactoryTests(TestCase):
    """Test cases for the transformation factory"""
    
    def setUp(self):
        # Reset the factory's processors
        TransformationFactory._processors = {}
        
    def test_register_processor(self):
        TransformationFactory.register(NormalizeProcessor)
        self.assertIn("NormalizeProcessor", TransformationFactory._processors)
        
    def test_get_processor(self):
        TransformationFactory.register(NormalizeProcessor)
        processor = TransformationFactory.get_processor("NormalizeProcessor")
        self.assertIsInstance(processor, NormalizeProcessor)
        
    def test_get_nonexistent_processor(self):
        with self.assertRaises(ValueError):
            TransformationFactory.get_processor("NonexistentProcessor")
            
    def test_list_processors(self):
        TransformationFactory.register(NormalizeProcessor)
        TransformationFactory.register(LogProcessor)
        
        processors = TransformationFactory.list_processors()
        self.assertIn("NormalizeProcessor", processors)
        self.assertIn("LogProcessor", processors)
        self.assertIn("description", processors["NormalizeProcessor"])
        self.assertIn("parameters", processors["NormalizeProcessor"])

class TransformationViewTests(TestCase):
    """Test cases for transformation views"""
    
    def setUp(self):
        self.client = Client()
        # Create a sample dataset for testing
        self.sample_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50]
        })
        self.dataset_name = 'test_dataset'
        save_dataset(self.dataset_name, self.sample_data.to_dict(orient="records"))
        
    def tearDown(self):
        delete_dataset(self.dataset_name)
        delete_dataset(f"{self.dataset_name}_transformed")
        
    def test_apply_transformation(self):
        """Test applying a transformation to a dataset"""
        data = {
            'transformation': 'NormalizeProcessor',
            'parameters': {
                'column': 'A'
            }
        }
        
        response = self.client.post(
            reverse('transformations:apply-transformation', args=[self.dataset_name]),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('message', response_data)
        self.assertIn('dataset', response_data)
        
        # Verify the transformed dataset
        transformed_dataset = get_dataset(f"{self.dataset_name}_transformed")
        self.assertIsNotNone(transformed_dataset)
        self.assertTrue(transformed_dataset['A'].min() == 0)
        self.assertTrue(transformed_dataset['A'].max() == 1)
        
    def test_apply_transformation_missing_field(self):
        """Test applying transformation with missing required field"""
        data = {
            'parameters': {
                'column': 'A'
            }
        }
        
        response = self.client.post(
            reverse('transformations:apply-transformation', args=[self.dataset_name]),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
        
    def test_apply_transformation_nonexistent_dataset(self):
        """Test applying transformation to nonexistent dataset"""
        data = {
            'transformation': 'NormalizeProcessor',
            'parameters': {
                'column': 'A'
            }
        }
        
        response = self.client.post(
            reverse('transformations:apply-transformation', args=['nonexistent']),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
        
    def test_apply_transformation_invalid_json(self):
        """Test applying transformation with invalid JSON"""
        response = self.client.post(
            reverse('transformations:apply-transformation', args=[self.dataset_name]),
            data='invalid json',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
        
    def test_list_available_transformations(self):
        """Test listing available transformations"""
        response = self.client.get(reverse('transformations:available-transformations'))
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('transformations', response_data)
        
        transformations = response_data['transformations']
        self.assertIn('NormalizeProcessor', transformations)
        self.assertIn('LogProcessor', transformations)
        self.assertIn('SquareRootProcessor', transformations)
        
        # Check structure of transformation details
        normalize_details = transformations['NormalizeProcessor']
        self.assertIn('description', normalize_details)
        self.assertIn('parameters', normalize_details) 