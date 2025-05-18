import pandas as pd
import plotly.express as px
from ..base import BaseVisualization

HEATMAP_PROPERTIES = {
    'name': 'heatmap',
    'description': 'Creates a heatmap to visualize correlation or frequency data',
    'parameters': {
        'x': 'Column name for x-axis',
        'y': 'Column name for y-axis',
        'z': 'Column name for color values (optional)',
        'title': 'Plot title (optional)',
        'x_label': 'X-axis label (optional)',
        'y_label': 'Y-axis label (optional)',
        'color_scale': 'Color scale to use (default: RdYlBu)',
        'text_auto': 'Whether to show text values (default: False)',
        'text_format': 'Text format for values (default: .2f)'
    }
}

class HeatmapPlot(BaseVisualization):
    def visualize(self, df: pd.DataFrame, x: str, y: str, z: str = None,
                 title: str = None, x_label: str = None, y_label: str = None,
                 color_scale: str = 'RdYlBu', text_auto: bool = False,
                 text_format: str = '.2f') -> dict:
        """
        Create a heatmap visualization
        
        Args:
            df (pd.DataFrame): The input dataframe
            x (str): Column name for x-axis
            y (str): Column name for y-axis
            z (str, optional): Column name for color values
            title (str, optional): Plot title
            x_label (str, optional): X-axis label
            y_label (str, optional): Y-axis label
            color_scale (str): Color scale to use
            text_auto (bool): Whether to show text values
            text_format (str): Text format for values
            
        Returns:
            dict: The visualization data and metadata
        """
        # Validate columns
        required_cols = [x, y]
        if z:
            required_cols.append(z)
            
        invalid_cols = [col for col in required_cols if col not in df.columns]
        if invalid_cols:
            raise ValueError(f"Columns not found in dataframe: {invalid_cols}")
        
        # Create the heatmap
        fig = px.density_heatmap(
            df,
            x=x,
            y=y,
            z=z,
            title=title or f"Heatmap of {y} vs {x}",
            labels={
                x: x_label or x,
                y: y_label or y,
                z: z or 'Count'
            },
            color_continuous_scale=color_scale,
            text_auto=text_auto
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title=x_label or x,
            yaxis_title=y_label or y
        )
        
        # Update text format if showing text
        if text_auto:
            fig.update_traces(texttemplate=f'%{{text:{text_format}}}')
        
        return self._create_figure(fig)
    
    @property
    def name(self) -> str:
        return HEATMAP_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return HEATMAP_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return HEATMAP_PROPERTIES['parameters'] 