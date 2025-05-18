import pandas as pd
import plotly.express as px
from ..base import BaseVisualization

BAR_PROPERTIES = {
    'name': 'bar',
    'description': 'Creates a bar plot to visualize categorical data',
    'parameters': {
        'x': 'Column name for x-axis (categories)',
        'y': 'Column name for y-axis (values)',
        'color': 'Column name for color encoding (optional)',
        'title': 'Plot title (optional)',
        'x_label': 'X-axis label (optional)',
        'y_label': 'Y-axis label (optional)',
        'orientation': 'Bar orientation: v (vertical) or h (horizontal) (default: v)',
        'sort_by': 'Column to sort bars by (optional)',
        'sort_ascending': 'Whether to sort in ascending order (default: True)'
    }
}

class BarPlot(BaseVisualization):
    def visualize(self, df: pd.DataFrame, x: str, y: str, color: str = None,
                 title: str = None, x_label: str = None, y_label: str = None,
                 orientation: str = 'v', sort_by: str = None, sort_ascending: bool = True) -> dict:
        """
        Create a bar plot visualization
        
        Args:
            df (pd.DataFrame): The input dataframe
            x (str): Column name for x-axis (categories)
            y (str): Column name for y-axis (values)
            color (str, optional): Column name for color encoding
            title (str, optional): Plot title
            x_label (str, optional): X-axis label
            y_label (str, optional): Y-axis label
            orientation (str): Bar orientation: v (vertical) or h (horizontal)
            sort_by (str, optional): Column to sort bars by
            sort_ascending (bool): Whether to sort in ascending order
            
        Returns:
            dict: The visualization data and metadata
        """
        # Validate columns
        required_cols = [x, y]
        if color:
            required_cols.append(color)
        if sort_by:
            required_cols.append(sort_by)
            
        invalid_cols = [col for col in required_cols if col not in df.columns]
        if invalid_cols:
            raise ValueError(f"Columns not found in dataframe: {invalid_cols}")
        
        # Sort data if requested
        if sort_by:
            df = df.sort_values(by=sort_by, ascending=sort_ascending)
        
        # Create the bar plot
        fig = px.bar(
            df,
            x=x,
            y=y,
            color=color,
            title=title or f"{y} by {x}",
            labels={
                x: x_label or x,
                y: y_label or y
            },
            orientation=orientation
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
        return BAR_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return BAR_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return BAR_PROPERTIES['parameters'] 