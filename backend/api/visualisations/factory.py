import importlib
from pathlib import Path

class VisualizationFactory:
    """Factory for creating visualizations dynamically."""
    _visualizers = None

    @classmethod
    def _initialize_visualizers(cls):
        """Lazy initialization to load visualizers only when first accessed."""
        if cls._visualizers is None:
            cls._visualizers = {}
            cls._register_default_visualizers()  # Register default visualizers
            cls._load_plugins("api.plugins")   # Load user-defined plugins (optional)

    @classmethod
    def _register_default_visualizers(cls):
        """Register default visualizers with error handling."""
        default_visualizers = {
            "bar": "api.visualisations.visualizers.BarVisualizer",
            "line": "api.visualisations.visualizers.LineVisualizer",
            "scatter": "api.visualisations.visualizers.ScatterVisualizer",
            "pie": "api.visualisations.visualizers.PieVisualizer",
            "histogram": "api.visualisations.visualizers.HistogramVisualizer",
            "box": "api.visualisations.visualizers.BoxVisualizer",
            "heatmap": "api.visualisations.visualizers.HeatmapVisualizer",
        }

        for viz_type, visualizer_class_path in default_visualizers.items():
            try:
                # Split the module and class name
                module_name, class_name = visualizer_class_path.rsplit(".", 1)
                module = importlib.import_module(module_name)
                visualizer_class = getattr(module, class_name)
                cls.register_visualizer(viz_type, visualizer_class)
            except (ImportError, AttributeError) as e:
                print(f"Failed to register visualizer {viz_type}: {e}")

    @classmethod
    def _load_plugins(cls, plugin_dir):
        """Load visualization plugins from the specified directory."""
        try:
            plugin_path = Path(importlib.import_module(plugin_dir).__file__).parent
            for item in plugin_path.iterdir():
                if item.is_dir() and (item / "__init__.py").exists():
                    try:
                        # Try to import the plugin module
                        plugin_module = importlib.import_module(f"{plugin_dir}.{item.name}")
                        
                        # Look for visualizer classes in the plugin
                        for attr_name in dir(plugin_module):
                            attr = getattr(plugin_module, attr_name)
                            if isinstance(attr, type) and hasattr(attr, "visualize"):
                                # Register the visualizer with its name
                                cls.register_visualizer(item.name, attr)
                    except Exception as e:
                        print(f"Failed to load plugin {item.name}: {e}")
        except ImportError:
            # Plugin directory doesn't exist or can't be imported
            pass

    @classmethod
    def register_visualizer(cls, viz_type, visualizer_class):
        """Register a new visualizer type."""
        cls._initialize_visualizers()
        cls._visualizers[viz_type] = visualizer_class

    @classmethod
    def get_visualizer(cls, viz_type):
        """Get a visualizer instance for the specified type."""
        cls._initialize_visualizers()
        if viz_type not in cls._visualizers:
            raise ValueError(f"Unsupported visualization type: {viz_type}")
        return cls._visualizers[viz_type]()

    @classmethod
    def list_visualizers(cls):
        """List all available visualizer types."""
        cls._initialize_visualizers()
        return list(cls._visualizers.keys())