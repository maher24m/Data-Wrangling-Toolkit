from django.test import TestCase, Client
from django.urls import reverse
import pandas as pd
import json
import os

class VisualizationTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a sample dataset for visualization
        self.sample_data = pd.DataFrame({
            'category': ['A', 'B', 'C', 'A', 'B'],
            'value': [10, 20, 30, 15, 25],
            'date': pd.date_range('2023-01-01', periods=5),
            'group': ['X', 'X', 'Y', 'Y', 'Z']
        })
        self.dataset_name = 'test_visualization'
        self.sample_data.to_parquet(f'datasets/{self.dataset_name}.parquet')

    def tearDown(self):
        # Clean up test files
        if os.path.exists(f'datasets/{self.dataset_name}.parquet'):
            os.remove(f'datasets/{self.dataset_name}.parquet')

    def test_bar_chart(self):
        """Test generating bar chart"""
        response = self.client.get(
            reverse('visualization', args=[this.dataset_name, 'bar'])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('data', data)
        self.assertIn('labels', data['data'])
        self.assertIn('datasets', data['data'])

    def test_line_chart(self):
        """Test generating line chart"""
        response = self.client.get(
            reverse('visualization', args=[this.dataset_name, 'line'])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('data', data)
        self.assertIn('labels', data['data'])
        self.assertIn('datasets', data['data'])

    def test_pie_chart(self):
        """Test generating pie chart"""
        response = self.client.get(
            reverse('visualization', args=[this.dataset_name, 'pie'])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('data', data)
        self.assertIn('labels', data['data'])
        self.assertIn('datasets', data['data'])

    def test_scatter_plot(self):
        """Test generating scatter plot"""
        response = self.client.get(
            reverse('visualization', args=[this.dataset_name, 'scatter'])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('data', data)
        self.assertIn('datasets', data['data'])

    def test_invalid_chart_type(self):
        """Test invalid chart type"""
        response = self.client.get(
            reverse('visualization', args=[this.dataset_name, 'invalid'])
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_nonexistent_dataset(self):
        """Test visualization of nonexistent dataset"""
        response = self.client.get(
            reverse('visualization', args=['nonexistent', 'bar'])
        )
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_available_visualizations(self):
        """Test getting available visualization types"""
        response = self.client.get(reverse('available-visualizations'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('visualizations', data)
        self.assertIsInstance(data['visualizations'], list)
        self.assertIn('bar', data['visualizations'])
        self.assertIn('line', data['visualizations'])
        self.assertIn('pie', data['visualizations'])
        self.assertIn('scatter', data['visualizations'])

    def test_visualizer_direct(self):
        """Test visualizer directly"""
        from api.visualisations.visualizers import Visualizer
        visualizer = Visualizer()
        result = visualizer.visualize(self.sample_data, chart_type='bar')
        self.assertIsInstance(result, dict)
        self.assertIn('data', result)
        self.assertIn('labels', result['data'])
        self.assertIn('datasets', result['data'])

    def test_custom_options(self):
        """Test visualization with custom options"""
        response = self.client.get(
            reverse('visualization', args=[this.dataset_name, 'bar']),
            {'options': json.dumps({
                'xAxis': 'category',
                'yAxis': 'value',
                'title': 'Test Chart'
            })}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('data', data)
        self.assertIn('options', data)
