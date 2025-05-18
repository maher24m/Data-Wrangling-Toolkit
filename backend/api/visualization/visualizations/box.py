import pandas as pd
import plotly.express as px
from ..base import BaseVisualization

BOX_PROPERTIES = {
    'name': 'box',
    'description': 'Creates a box plot to visualize the distribution of numeric data by categories',
    'parameters': {
        'x': 'Column name for x-axis (categories)',
        'y': 'Column name for y-axis (values)',
        'color': 'Column name for color encoding (optional)',
        'title': 'Plot title (optional)',
        'x_label': 'X-axis label (optional)',
        'y_label': 'Y-axis label (optional)',
        'points': 'Whether to show individual points: all, outliers, or none (default: outliers)',
        'notched': 'Whether to show notched box plots (default: False)'
    }
}

class BoxPlot(BaseVisualization):
    def visualize(self, df: pd.DataFrame, x: str, y: str, color: str = None,
                 title: str = None, x_label: str = None, y_label: str = None,
                 points: str = 'outliers', notched: bool = False) -> dict:
        """
        Create a box plot visualization
        
        Args:
            df (pd.DataFrame): The input dataframe
            x (str): Column name for x-axis (categories)
            y (str): Column name for y-axis (values)
            color (str, optional): Column name for color encoding
            title (str, optional): Plot title
            x_label (str, optional): X-axis label
            y_label (str, optional): Y-axis label
            points (str): Whether to show individual points: all, outliers, or none
            notched (bool): Whether to show notched box plots
            
        Returns:
            dict: The visualization data and metadata
        """
        # Validate columns
        required_cols = [x, y]
        if color:
            required_cols.append(color)
            
        invalid_cols = [col for col in required_cols if col not in df.columns]
        if invalid_cols:
            raise ValueError(f"Columns not found in dataframe: {invalid_cols}")
        
        # Create the box plot
        fig = px.box(
            df,
            x=x,
            y=y,
            color=color,
            title=title or f"Distribution of {y} by {x}",
            labels={
                x: x_label or x,
                y: y_label or y
            },
            points=points,
            notched=notched
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title=x_label or x,
            yaxis_title=y_label or y,
            showlegend=True if color else False
        )
        
        return self._create_figure(fig)
    
    @property
    def name(self) -> str:
        return BOX_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return BOX_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return BOX_PROPERTIES['parameters'] 