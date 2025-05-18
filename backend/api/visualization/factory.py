import importlib
from pathlib import Path
from typing import Dict, Type, Any, Optional
from .base import BaseVisualization
import pandas as pd

class VisualizationFactory:
    """Factory for managing visualizations with plugin support"""
    _visualizations: Optional[Dict[str, Type[BaseVisualization]]] = None

    @classmethod
    def _initialize_visualizations(cls):
        """Lazy initialization to load visualizations only when first accessed"""
        if cls._visualizations is None:
            cls._visualizations = {}
            cls._register_default_visualizations()
            cls._load_plugins("api.plugins.visualizations")

    @classmethod
    def _register_default_visualizations(cls):
        """Register default visualizations with error handling"""
        default_visualizations = {
            "scatter": "api.visualization.visualizations.scatter.ScatterPlot",
            "line": "api.visualization.visualizations.line.LinePlot",
            "bar": "api.visualization.visualizations.bar.BarPlot",
            "histogram": "api.visualization.visualizations.histogram.HistogramPlot",
            "box": "api.visualization.visualizations.box.BoxPlot",
            "heatmap": "api.visualization.visualizations.heatmap.HeatmapPlot"
        }

        for name, visualization_class_path in default_visualizations.items():
            try:
                module_name, class_name = visualization_class_path.rsplit(".", 1)
                module = importlib.import_module(module_name)
                visualization_class = getattr(module, class_name)
                
                if not issubclass(visualization_class, BaseVisualization):
                    raise TypeError(
                        f"Visualization class must inherit from BaseVisualization: {visualization_class.__name__}"
                    )
                
                cls._visualizations[name] = visualization_class
                print(f"Successfully registered visualization: {name} -> {visualization_class.__name__}")
            except Exception as e:
                print(f"Error registering visualization '{name}': {e}")

    @classmethod
    def get_visualization(cls, name: str) -> BaseVisualization:
        """Get a visualization by name"""
        cls._initialize_visualizations()
        if name not in cls._visualizations:
            raise ValueError(f"Visualization {name} not found")
        return cls._visualizations[name]()

    @classmethod
    def list_visualizations(cls) -> Dict[str, Dict[str, Any]]:
        """List all available visualizations with their descriptions and parameters"""
        cls._initialize_visualizations()
        return {
            name: {
                'description': visualization().description,
                'parameters': visualization().parameters
            }
            for name, visualization in cls._visualizations.items()
        }

    @classmethod
    def _load_plugins(cls, plugin_dir: str):
        """
        Dynamically load visualization plugins from a directory
        
        Args:
            plugin_dir (str): The directory path to load plugins from
        """
        try:
            # Convert string path to Path object for better path handling
            plugin_path = Path(plugin_dir)
            
            # Check if the plugin directory exists
            if not plugin_path.exists():
                print(f"Plugin directory {plugin_dir} not found. Skipping plugin loading.")
                return

            # Iterate through all Python files in the plugin directory
            for module_file in plugin_path.glob("*.py"):
                # Skip __init__.py files
                if module_file.name == "__init__.py":
                    continue

                try:
                    # Get the module name without the .py extension
                    module_name = module_file.stem
                    # Construct the full module path
                    full_module_path = f"{plugin_dir}.{module_name}"
                    
                    # Import the module
                    module = importlib.import_module(full_module_path)
                    
                    # Look for visualization classes in the module
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        
                        # Check if the attribute is a visualization class
                        if (
                            isinstance(attr, type)  # Is it a class?
                            and issubclass(attr, BaseVisualization)  # Is it a visualization?
                            and attr != BaseVisualization  # Is it not the base class?
                        ):
                            # Get the visualization name
                            visualization_name = getattr(attr, "name", None)
                            
                            if visualization_name:
                                # Check if this visualization would override an existing one
                                if visualization_name in cls._visualizations:
                                    print(
                                        f"Warning: Plugin visualization '{visualization_name}' "
                                        f"from {full_module_path} overrides existing visualization"
                                    )
                                
                                # Register the visualization
                                cls._visualizations[visualization_name] = attr
                                print(
                                    f"Successfully loaded plugin visualization: "
                                    f"{visualization_name} -> {attr.__name__}"
                                )
                            else:
                                print(
                                    f"Warning: Visualization class {attr.__name__} in {full_module_path} "
                                    f"lacks 'name' attribute. Skipping registration."
                                )
                                
                except ImportError as e:
                    print(f"Error importing plugin module {module_name}: {e}")
                except Exception as e:
                    print(f"Error loading plugin from {module_file.name}: {e}")
                    
        except Exception as e:
            print(f"Unexpected error during plugin loading: {e}") 