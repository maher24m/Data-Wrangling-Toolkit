import pandas as pd
import plotly.express as px
from ..base import BaseVisualization

SCATTER_PROPERTIES = {
    'name': 'scatter',
    'description': 'Creates a scatter plot to visualize relationships between two numeric variables',
    'parameters': {
        'x': 'Column name for x-axis',
        'y': 'Column name for y-axis',
        'color': 'Column name for color encoding (optional)',
        'size': 'Column name for size encoding (optional)',
        'title': 'Plot title (optional)',
        'x_label': 'X-axis label (optional)',
        'y_label': 'Y-axis label (optional)'
    }
}

class ScatterPlot(BaseVisualization):
    def visualize(self, df: pd.DataFrame, x: str, y: str, color: str = None, size: str = None,
                 title: str = None, x_label: str = None, y_label: str = None) -> dict:
        """
        Create a scatter plot visualization
        
        Args:
            df (pd.DataFrame): The input dataframe
            x (str): Column name for x-axis
            y (str): Column name for y-axis
            color (str, optional): Column name for color encoding
            size (str, optional): Column name for size encoding
            title (str, optional): Plot title
            x_label (str, optional): X-axis label
            y_label (str, optional): Y-axis label
            
        Returns:
            dict: The visualization data and metadata
        """
        # Validate columns
        required_cols = [x, y]
        if color:
            required_cols.append(color)
        if size:
            required_cols.append(size)
            
        invalid_cols = [col for col in required_cols if col not in df.columns]
        if invalid_cols:
            raise ValueError(f"Columns not found in dataframe: {invalid_cols}")
        
        # Create the scatter plot
        fig = px.scatter(
            df,
            x=x,
            y=y,
            color=color,
            size=size,
            title=title or f"{y} vs {x}",
            labels={
                x: x_label or x,
                y: y_label or y
            }
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
        return SCATTER_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return SCATTER_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return SCATTER_PROPERTIES['parameters'] 