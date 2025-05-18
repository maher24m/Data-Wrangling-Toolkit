import pandas as pd
import plotly.express as px
from ..base import BaseVisualization

HISTOGRAM_PROPERTIES = {
    'name': 'histogram',
    'description': 'Creates a histogram to visualize the distribution of a numeric variable',
    'parameters': {
        'x': 'Column name for the variable to plot',
        'color': 'Column name for color encoding (optional)',
        'title': 'Plot title (optional)',
        'x_label': 'X-axis label (optional)',
        'y_label': 'Y-axis label (optional)',
        'nbins': 'Number of bins (optional)',
        'normalize': 'Whether to normalize the histogram (default: False)',
        'cumulative': 'Whether to show cumulative distribution (default: False)'
    }
}

class HistogramPlot(BaseVisualization):
    def visualize(self, df: pd.DataFrame, x: str, color: str = None,
                 title: str = None, x_label: str = None, y_label: str = None,
                 nbins: int = None, normalize: bool = False, cumulative: bool = False) -> dict:
        """
        Create a histogram visualization
        
        Args:
            df (pd.DataFrame): The input dataframe
            x (str): Column name for the variable to plot
            color (str, optional): Column name for color encoding
            title (str, optional): Plot title
            x_label (str, optional): X-axis label
            y_label (str, optional): Y-axis label
            nbins (int, optional): Number of bins
            normalize (bool): Whether to normalize the histogram
            cumulative (bool): Whether to show cumulative distribution
            
        Returns:
            dict: The visualization data and metadata
        """
        # Validate columns
        required_cols = [x]
        if color:
            required_cols.append(color)
            
        invalid_cols = [col for col in required_cols if col not in df.columns]
        if invalid_cols:
            raise ValueError(f"Columns not found in dataframe: {invalid_cols}")
        
        # Create the histogram
        fig = px.histogram(
            df,
            x=x,
            color=color,
            title=title or f"Distribution of {x}",
            labels={
                x: x_label or x,
                'count': y_label or 'Count'
            },
            nbins=nbins,
            histnorm='percent' if normalize else None,
            cumulative=cumulative
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title=x_label or x,
            yaxis_title=y_label or ('Percentage' if normalize else 'Count'),
            showlegend=True if color else False
        )
        
        return self._create_figure(fig)
    
    @property
    def name(self) -> str:
        return HISTOGRAM_PROPERTIES['name']
    
    @property
    def description(self) -> str:
        return HISTOGRAM_PROPERTIES['description']
    
    @property
    def parameters(self) -> dict:
        return HISTOGRAM_PROPERTIES['parameters'] 