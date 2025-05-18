import pandas as pd
import plotly.express as px
from ..base import BaseVisualization

LINE_PROPERTIES = {
    'name': 'line',
    'description': 'Creates a line plot to visualize trends over time or ordered categories',
    'parameters': {
        'x': 'Column name for x-axis',
        'y': 'Column name for y-axis',
        'color': 'Column name for color encoding (optional)',
        'title': 'Plot title (optional)',
        'x_label': 'X-axis label (optional)',
        'y_label': 'Y-axis label (optional)',
        'markers': 'Whether to show markers on lines (default: True)'
    }
}

class LinePlot(BaseVisualization):
    def visualize(self, df: pd.DataFrame, x: str, y: str, color: str = None,
                 title: str = None, x_label: str = None, y_label: str = None,
                 markers: bool = True) -> dict:
        """
        Create a line plot visualization
        
        Args:
            df (pd.DataFrame): The input dataframe
            x (str): Column name for x-axis
            y (str): Column name for y-axis
            color (str, optional): Column name for color encoding
            title (str, optional): Plot title
            x_label (str, optional): X-axis label
            y_label (str, optional): Y-axis label
            markers (bool): Whether to show markers on lines
            
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
        
        # Create the line plot
        fig = px.line(
            df,
            x=x,
            y=y,
            color=color,
            title=title or f"{y} over {x}",
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
        
        # Update traces to show/hide markers
        fig.update_traces(mode='lines+markers' if markers else 'lines')
        
        return self._create_figure(fig)
    
    @property
    def name(self) -> str:
        return LINE_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return LINE_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return LINE_PROPERTIES['parameters'] 