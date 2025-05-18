import importlib
from pathlib import Path
from typing import Dict, Type, Any, Optional
from .base import BaseAnalysis
import pandas as pd

class AnalysisFactory:
    """Factory for managing analyses with plugin support"""
    _analyses: Optional[Dict[str, Type[BaseAnalysis]]] = None

    @classmethod
    def _initialize_analyses(cls):
        """Lazy initialization to load analyses only when first accessed"""
        if cls._analyses is None:
            cls._analyses = {}
            cls._register_default_analyses()
            cls._load_plugins("api.plugins.analyses")

    @classmethod
    def _register_default_analyses(cls):
        """Register default analyses with error handling"""
        default_analyses = {
            "descriptive": "api.analysis.analyses.descriptive.DescriptiveAnalysis",
            "correlation": "api.analysis.analyses.correlation.CorrelationAnalysis",
            "distribution": "api.analysis.analyses.distribution.DistributionAnalysis"
        }

        for name, analysis_class_path in default_analyses.items():
            try:
                module_name, class_name = analysis_class_path.rsplit(".", 1)
                module = importlib.import_module(module_name)
                analysis_class = getattr(module, class_name)
                
                if not issubclass(analysis_class, BaseAnalysis):
                    raise TypeError(
                        f"Analysis class must inherit from BaseAnalysis: {analysis_class.__name__}"
                    )
                
                cls._analyses[name] = analysis_class
                print(f"Successfully registered analysis: {name} -> {analysis_class.__name__}")
            except Exception as e:
                print(f"Error registering analysis '{name}': {e}")

    @classmethod
    def get_analysis(cls, name: str) -> BaseAnalysis:
        """Get an analysis by name"""
        cls._initialize_analyses()
        if name not in cls._analyses:
            raise ValueError(f"Analysis {name} not found")
        return cls._analyses[name]()

    @classmethod
    def list_analyses(cls) -> Dict[str, Dict[str, Any]]:
        """List all available analyses with their descriptions and parameters"""
        cls._initialize_analyses()
        return {
            name: {
                'description': analysis().description,
                'parameters': analysis().parameters
            }
            for name, analysis in cls._analyses.items()
        }

    @classmethod
    def _load_plugins(cls, plugin_dir: str):
        """
        Dynamically load analysis plugins from a directory
        
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
                    
                    # Look for analysis classes in the module
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        
                        # Check if the attribute is an analysis class
                        if (
                            isinstance(attr, type)  # Is it a class?
                            and issubclass(attr, BaseAnalysis)  # Is it an analysis?
                            and attr != BaseAnalysis  # Is it not the base class?
                        ):
                            # Get the analysis name
                            analysis_name = getattr(attr, "name", None)
                            
                            if analysis_name:
                                # Check if this analysis would override an existing one
                                if analysis_name in cls._analyses:
                                    print(
                                        f"Warning: Plugin analysis '{analysis_name}' "
                                        f"from {full_module_path} overrides existing analysis"
                                    )
                                
                                # Register the analysis
                                cls._analyses[analysis_name] = attr
                                print(
                                    f"Successfully loaded plugin analysis: "
                                    f"{analysis_name} -> {attr.__name__}"
                                )
                            else:
                                print(
                                    f"Warning: Analysis class {attr.__name__} in {full_module_path} "
                                    f"lacks 'name' attribute. Skipping registration."
                                )
                                
                except ImportError as e:
                    print(f"Error importing plugin module {module_name}: {e}")
                except Exception as e:
                    print(f"Error loading plugin from {module_file.name}: {e}")
                    
        except Exception as e:
            print(f"Unexpected error during plugin loading: {e}") 