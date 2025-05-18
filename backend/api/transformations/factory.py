import importlib
from pathlib import Path
from typing import Dict, Type, Any, Optional
from .base import BaseTransformation
import pandas as pd

class TransformationFactory:
    """Factory for managing transformations with plugin support"""
    _transformations: Optional[Dict[str, Type[BaseTransformation]]] = None

    @classmethod
    def _initialize_transformations(cls):
        """Lazy initialization to load transformations only when first accessed"""
        if cls._transformations is None:
            cls._transformations = {}
            cls._register_default_transformations()
            cls._load_plugins("api.plugins.transformations")

    @classmethod
    def _register_default_transformations(cls):
        """Register default transformations with error handling"""
        default_transformations = {
            "normalize": "api.transformations.transformations.normalize.NormalizeTransformation",
            "log": "api.transformations.transformations.log.LogTransformation",
            "square_root": "api.transformations.transformations.square_root.SquareRootTransformation"
        }

        for name, transformation_class_path in default_transformations.items():
            try:
                module_name, class_name = transformation_class_path.rsplit(".", 1)
                module = importlib.import_module(module_name)
                transformation_class = getattr(module, class_name)
                
                if not issubclass(transformation_class, BaseTransformation):
                    raise TypeError(
                        f"Transformation class must inherit from BaseTransformation: {transformation_class.__name__}"
                    )
                
                cls._transformations[name] = transformation_class
                print(f"Successfully registered transformation: {name} -> {transformation_class.__name__}")
            except Exception as e:
                print(f"Error registering transformation '{name}': {e}")

    @classmethod
    def get_transformation(cls, name: str) -> BaseTransformation:
        """Get a transformation by name"""
        cls._initialize_transformations()
        if name not in cls._transformations:
            raise ValueError(f"Transformation {name} not found")
        return cls._transformations[name]()

    @classmethod
    def list_transformations(cls) -> Dict[str, Dict[str, Any]]:
        """List all available transformations with their descriptions and parameters"""
        cls._initialize_transformations()
        return {
            name: {
                'description': transformation().description,
                'parameters': transformation().parameters
            }
            for name, transformation in cls._transformations.items()
        }

    @classmethod
    def _load_plugins(cls, plugin_dir: str):
        """
        Dynamically load transformation plugins from a directory
        
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
                    
                    # Look for transformation classes in the module
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        
                        # Check if the attribute is a transformation class
                        if (
                            isinstance(attr, type)  # Is it a class?
                            and issubclass(attr, BaseTransformation)  # Is it a transformation?
                            and attr != BaseTransformation  # Is it not the base class?
                        ):
                            # Get the transformation name
                            transformation_name = getattr(attr, "name", None)
                            
                            if transformation_name:
                                # Check if this transformation would override an existing one
                                if transformation_name in cls._transformations:
                                    print(
                                        f"Warning: Plugin transformation '{transformation_name}' "
                                        f"from {full_module_path} overrides existing transformation"
                                    )
                                
                                # Register the transformation
                                cls._transformations[transformation_name] = attr
                                print(
                                    f"Successfully loaded plugin transformation: "
                                    f"{transformation_name} -> {attr.__name__}"
                                )
                            else:
                                print(
                                    f"Warning: Transformation class {attr.__name__} in {full_module_path} "
                                    f"lacks 'name' attribute. Skipping registration."
                                )
                                
                except ImportError as e:
                    print(f"Error importing plugin module {module_name}: {e}")
                except Exception as e:
                    print(f"Error loading plugin from {module_file.name}: {e}")
                    
        except Exception as e:
            print(f"Unexpected error during plugin loading: {e}")
