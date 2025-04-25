# api/visualisations/visualizers.py

import pandas as pd
import numpy as np
import json

class Visualizer:
    """Base class for all data visualizers"""
    def visualize(self, data, **kwargs):
        """
        Generate visualization data from the dataset
        
        Args:
            data: DataFrame containing the data to visualize
            **kwargs: Additional parameters for the visualization
            
        Returns:
            dict: Visualization data in a format suitable for frontend rendering
        """
        raise NotImplementedError("Subclasses must implement this method")

class BarVisualizer(Visualizer):
    def visualize(self, data, **kwargs):
        """
        Generate bar chart data
        
        Args:
            data: DataFrame containing the data
            **kwargs: 
                - column: Column to use for the bar chart (default: first column)
                - group_by: Column to group by (optional)
                - aggregation: Aggregation function (count, sum, mean, etc.)
        """
        column = kwargs.get('column', data.columns[0])
        group_by = kwargs.get('group_by')
        aggregation = kwargs.get('aggregation', 'count')
        
        if group_by:
            if aggregation == 'count':
                chart_data = data.groupby(group_by)[column].count().to_dict()
            elif aggregation == 'sum':
                chart_data = data.groupby(group_by)[column].sum().to_dict()
            elif aggregation == 'mean':
                chart_data = data.groupby(group_by)[column].mean().to_dict()
            else:
                chart_data = data.groupby(group_by)[column].count().to_dict()
        else:
            chart_data = data[column].value_counts().to_dict()
            
        return {
            'type': 'bar',
            'data': {
                'labels': list(chart_data.keys()),
                'values': list(chart_data.values())
            }
        }

class LineVisualizer(Visualizer):
    def visualize(self, data, **kwargs):
        """
        Generate line chart data
        
        Args:
            data: DataFrame containing the data
            **kwargs:
                - x_column: Column to use for x-axis
                - y_column: Column to use for y-axis
                - group_by: Column to group by (optional)
        """
        x_column = kwargs.get('x_column', data.columns[0])
        y_column = kwargs.get('y_column', data.columns[1] if len(data.columns) > 1 else data.columns[0])
        group_by = kwargs.get('group_by')
        
        if group_by:
            # Group by the specified column and calculate mean for each group
            grouped_data = data.groupby(group_by)[y_column].mean().reset_index()
            chart_data = {
                'labels': grouped_data[group_by].tolist(),
                'values': grouped_data[y_column].tolist()
            }
        else:
            # Sort by x_column and use y_column values
            sorted_data = data.sort_values(by=x_column)
            chart_data = {
                'labels': sorted_data[x_column].tolist(),
                'values': sorted_data[y_column].tolist()
            }
            
        return {
            'type': 'line',
            'data': chart_data
        }

class ScatterVisualizer(Visualizer):
    def visualize(self, data, **kwargs):
        """
        Generate scatter plot data
        
        Args:
            data: DataFrame containing the data
            **kwargs:
                - x_column: Column to use for x-axis
                - y_column: Column to use for y-axis
                - color_by: Column to use for coloring points (optional)
        """
        x_column = kwargs.get('x_column', data.columns[0])
        y_column = kwargs.get('y_column', data.columns[1] if len(data.columns) > 1 else data.columns[0])
        color_by = kwargs.get('color_by')
        
        chart_data = {
            'x': data[x_column].tolist(),
            'y': data[y_column].tolist()
        }
        
        if color_by:
            chart_data['colors'] = data[color_by].tolist()
            
        return {
            'type': 'scatter',
            'data': chart_data
        }

class PieVisualizer(Visualizer):
    def visualize(self, data, **kwargs):
        """
        Generate pie chart data
        
        Args:
            data: DataFrame containing the data
            **kwargs:
                - column: Column to use for the pie chart
        """
        column = kwargs.get('column', data.columns[0])
        
        # Count occurrences of each value in the column
        value_counts = data[column].value_counts()
        
        chart_data = {
            'labels': value_counts.index.tolist(),
            'values': value_counts.values.tolist()
        }
            
        return {
            'type': 'pie',
            'data': chart_data
        }

class HistogramVisualizer(Visualizer):
    def visualize(self, data, **kwargs):
        """
        Generate histogram data
        
        Args:
            data: DataFrame containing the data
            **kwargs:
                - column: Column to use for the histogram
                - bins: Number of bins (default: 10)
        """
        column = kwargs.get('column', data.columns[0])
        bins = kwargs.get('bins', 10)
        
        # Calculate histogram
        hist, bin_edges = np.histogram(data[column].dropna(), bins=bins)
        
        # Calculate bin centers
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        chart_data = {
            'labels': bin_centers.tolist(),
            'values': hist.tolist()
        }
            
        return {
            'type': 'histogram',
            'data': chart_data
        }

class BoxVisualizer(Visualizer):
    def visualize(self, data, **kwargs):
        """
        Generate box plot data
        
        Args:
            data: DataFrame containing the data
            **kwargs:
                - column: Column to use for the box plot
                - group_by: Column to group by (optional)
        """
        column = kwargs.get('column', data.columns[0])
        group_by = kwargs.get('group_by')
        
        if group_by:
            # Group by the specified column and calculate statistics for each group
            grouped_data = data.groupby(group_by)[column].apply(lambda x: {
                'min': x.min(),
                'q1': x.quantile(0.25),
                'median': x.median(),
                'q3': x.quantile(0.75),
                'max': x.max()
            }).to_dict()
            
            chart_data = {
                'groups': list(grouped_data.keys()),
                'stats': list(grouped_data.values())
            }
        else:
            # Calculate statistics for the entire column
            stats = {
                'min': data[column].min(),
                'q1': data[column].quantile(0.25),
                'median': data[column].median(),
                'q3': data[column].quantile(0.75),
                'max': data[column].max()
            }
            
            chart_data = {
                'groups': [column],
                'stats': [stats]
            }
            
        return {
            'type': 'box',
            'data': chart_data
        }

class HeatmapVisualizer(Visualizer):
    def visualize(self, data, **kwargs):
        """
        Generate heatmap data (correlation matrix)
        
        Args:
            data: DataFrame containing the data
            **kwargs:
                - columns: List of columns to include (default: all numeric columns)
        """
        columns = kwargs.get('columns')
        
        # Select numeric columns if not specified
        if not columns:
            numeric_data = data.select_dtypes(include=['number'])
            columns = numeric_data.columns.tolist()
        
        # Calculate correlation matrix
        corr_matrix = data[columns].corr()
        
        chart_data = {
            'labels': columns,
            'values': corr_matrix.values.tolist()
        }
            
        return {
            'type': 'heatmap',
            'data': chart_data
        } 