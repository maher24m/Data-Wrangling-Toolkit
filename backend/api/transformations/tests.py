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
from .base import BaseTransformation
from .transformations.normalize import NormalizeTransformation

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
        self.assertTrue(all(isinstance(x, str) for x in df['date']))

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
        self.assertIn('message', data)
        df = pd.read_parquet(f'datasets/{self.dataset_name}.parquet')
        self.assertTrue(all(df['numeric'] == [2, 4, 6, 8, 10]))

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
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

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
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_available_transformations(self):
        """Test getting available transformation types"""
        response = self.client.get(reverse('transformations:available-transformations'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('transformations', data)
        self.assertIsInstance(data['transformations'], dict)
        self.assertIn('NormalizeProcessor', data['transformations'])
        self.assertIn('LogProcessor', data['transformations'])
        self.assertIn('SquareRootProcessor', data['transformations'])

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
        """Reset the factory's transformations before each test"""
        TransformationFactory._transformations = None
        
    def test_register_default_transformations(self):
        """Test that default transformations are registered correctly"""
        TransformationFactory._initialize_transformations()
        
        # Check if default transformations are registered
        self.assertIn("normalize", TransformationFactory._transformations)
        self.assertIn("log", TransformationFactory._transformations)
        self.assertIn("square_root", TransformationFactory._transformations)
        
        # Verify transformation types
        self.assertIsInstance(
            TransformationFactory._transformations["normalize"],
            type(NormalizeTransformation)
        )
    
    def test_get_transformation(self):
        """Test getting a transformation instance"""
        transformation = TransformationFactory.get_transformation("normalize")
        self.assertIsInstance(transformation, NormalizeTransformation)
    
    def test_get_nonexistent_transformation(self):
        """Test getting a non-existent transformation raises error"""
        with self.assertRaises(ValueError) as context:
            TransformationFactory.get_transformation("nonexistent")
        self.assertIn("not found", str(context.exception))
    
    def test_list_transformations(self):
        """Test listing available transformations"""
        transformations = TransformationFactory.list_transformations()
        
        # Check structure of returned data
        self.assertIn("normalize", transformations)
        self.assertIn("description", transformations["normalize"])
        self.assertIn("parameters", transformations["normalize"])
        
        # Verify content
        self.assertIn("column", transformations["normalize"]["parameters"])
        self.assertIn("method", transformations["normalize"]["parameters"])

# class NormalizeTransformationTests(TestCase):
#     """Test cases for the normalize transformation"""
    
#     def setUp(self):
#         self.transformation = NormalizeTransformation()
#         self.df = pd.DataFrame({
#             "value": [1, 2, 3, 4, 5],
#             "other": [10, 20, 30, 40, 50]
#         })
    
#     def test_minmax_normalization(self):
#         """Test minmax normalization with default range"""
#         params = NormalizeParameters(
#             column="value",
#             method="minmax"
#         )
#         result = self.transformation.transform(self.df, params)
        
#         # Verify normalization results
#         self.assertTrue(np.all(result["value"] >= 0))
#         self.assertTrue(np.all(result["value"] <= 1))
#         self.assertEqual(result["value"].min(), 0)
#         self.assertEqual(result["value"].max(), 1)
    
#     def test_minmax_normalization_custom_range(self):
#         """Test minmax normalization with custom range"""
#         params = NormalizeParameters(
#             column="value",
#             method="minmax",
#             target_range=(-1, 1)
#         )
#         result = self.transformation.transform(self.df, params)
        
#         # Verify normalization results
#         self.assertTrue(np.all(result["value"] >= -1))
#         self.assertTrue(np.all(result["value"] <= 1))
#         self.assertEqual(result["value"].min(), -1)
#         self.assertEqual(result["value"].max(), 1)
    
#     def test_zscore_normalization(self):
#         """Test zscore normalization"""
#         params = NormalizeParameters(
#             column="value",
#             method="zscore"
#         )
#         result = self.transformation.transform(self.df, params)
        
#         # Verify z-score properties
#         self.assertAlmostEqual(result["value"].mean(), 0, places=10)
#         self.assertAlmostEqual(result["value"].std(), 1, places=10)
    
#     def test_robust_normalization(self):
#         """Test robust normalization"""
#         params = NormalizeParameters(
#             column="value",
#             method="robust"
#         )
#         result = self.transformation.transform(self.df, params)
        
#         # Verify robust normalization properties
#         self.assertAlmostEqual(result["value"].median(), 0, places=10)
    
#     def test_invalid_column(self):
#         """Test handling of invalid column name"""
#         params = NormalizeParameters(
#             column="nonexistent",
#             method="minmax"
#         )
#         with self.assertRaises(ValueError) as context:
#             self.transformation.transform(self.df, params)
#         self.assertIn("not found", str(context.exception))
    
#     def test_invalid_method(self):
#         """Test handling of invalid normalization method"""
#         params = NormalizeParameters(
#             column="value",
#             method="invalid_method"
#         )
#         with self.assertRaises(ValueError) as context:
#             self.transformation.transform(self.df, params)
#         self.assertIn("method", str(context.exception))

class TransformationIntegrationTests(TestCase):
    """Integration tests for the transformation system"""
    
    def setUp(self):
        TransformationFactory._transformations = None
        self.df = pd.DataFrame({
            "value": [1, 2, 3, 4, 5],
            "other": [10, 20, 30, 40, 50]
        })
    
    def test_apply_transformation(self):
        """Test applying a transformation through the factory"""
        result = TransformationFactory.apply_transformation(
            self.df,
            "normalize",
            {
                "column": "value",
                "method": "minmax"
            }
        )
        
        # Verify the result
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(np.all(result["value"] >= 0))
        self.assertTrue(np.all(result["value"] <= 1))
    
    def test_apply_transformation_invalid_params(self):
        """Test applying transformation with invalid parameters"""
        with self.assertRaises(ValueError) as context:
            TransformationFactory.apply_transformation(
                self.df,
                "normalize",
                {
                    "column": "value",
                    "method": "invalid_method"
                }
            )
        self.assertIn("method", str(context.exception))
    
    def test_apply_transformation_nonexistent(self):
        """Test applying non-existent transformation"""
        with self.assertRaises(ValueError) as context:
            TransformationFactory.apply_transformation(
                self.df,
                "nonexistent",
                {}
            )
        self.assertIn("not found", str(context.exception))
    
    def test_multiple_transformations(self):
        """Test applying multiple transformations in sequence"""
        # First normalize
        result = TransformationFactory.apply_transformation(
            self.df,
            "normalize",
            {
                "column": "value",
                "method": "minmax"
            }
        )
        
        # Then apply log transformation if available
        if "log" in TransformationFactory.list_transformations():
            result = TransformationFactory.apply_transformation(
                result,
                "log",
                {
                    "column": "value"
                }
            )
            
            # Verify the result
            self.assertIsInstance(result, pd.DataFrame)
            self.assertTrue(np.all(result["value"] >= 0))  # Log should be positive

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