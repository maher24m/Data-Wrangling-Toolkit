# backend/api/datacleaning/factory.py
import importlib
from pathlib import Path
from typing import Dict, Type, Any, Optional
from .base import BaseCleaning
import pandas as pd

class DataCleaningFactory:
    """Factory for managing data cleaning operations with plugin support"""
    _cleaners: Optional[Dict[str, Type[BaseCleaning]]] = None

    @classmethod
    def _initialize_cleaners(cls):
        """Lazy initialization to load cleaners only when first accessed"""
        if cls._cleaners is None:
            cls._cleaners = {}
            cls._register_default_cleaners()
            cls._load_plugins("api.plugins.cleaning")

    @classmethod
    def _register_default_cleaners(cls):
        """Register default cleaning operations with error handling"""
        default_cleaners = {
            "missing_values": "api.datacleaning.cleanings.missing_values.MissingValuesCleaning",
            "remove_duplicates": "api.datacleaning.cleanings.remove_duplicates.RemoveDuplicatesCleaning",
            "detect_outliers": "api.datacleaning.cleanings.detect_outliers.DetectOutliersCleaning",
            "replace_outliers": "api.datacleaning.cleanings.replace_outliers.ReplaceOutliersCleaning",
            "standardize_format": "api.datacleaning.cleanings.standardize_format.StandardizeFormatCleaning"
        }

        for name, cleaner_class_path in default_cleaners.items():
            try:
                module_name, class_name = cleaner_class_path.rsplit(".", 1)
                module = importlib.import_module(module_name)
                cleaner_class = getattr(module, class_name)
                
                if not issubclass(cleaner_class, BaseCleaning):
                    raise TypeError(
                        f"Cleaning class must inherit from BaseCleaning: {cleaner_class.__name__}"
                    )
                
                cls._cleaners[name] = cleaner_class
                print(f"Successfully registered cleaner: {name} -> {cleaner_class.__name__}")
            except Exception as e:
                print(f"Error registering cleaner '{name}': {e}")

    @classmethod
    def get_cleaner(cls, name: str) -> BaseCleaning:
        """Get a cleaner by name"""
        cls._initialize_cleaners()
        if name not in cls._cleaners:
            raise ValueError(f"Cleaning operation {name} not found {cls._cleaners}")
        return cls._cleaners[name]()

    @classmethod
    def list_cleaners(cls) -> Dict[str, Dict[str, Any]]:
        """List all available cleaning operations with their descriptions and parameters"""
        cls._initialize_cleaners()
        return {
            name: {
                'description': cleaner().description,
                'parameters': cleaner().parameters
            }
            for name, cleaner in cls._cleaners.items()
        }

    @classmethod
    def _load_plugins(cls, plugin_dir: str):
        """
        Dynamically load cleaning plugins from a directory
        
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
                    
                    # Look for cleaning classes in the module
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        
                        # Check if the attribute is a cleaning class
                        if (
                            isinstance(attr, type)  # Is it a class?
                            and issubclass(attr, BaseCleaning)  # Is it a cleaner?
                            and attr != BaseCleaning  # Is it not the base class?
                        ):
                            # Get the cleaning name
                            cleaning_name = getattr(attr, "name", None)
                            
                            if cleaning_name:
                                # Check if this cleaning would override an existing one
                                if cleaning_name in cls._cleaners:
                                    print(
                                        f"Warning: Plugin cleaning '{cleaning_name}' "
                                        f"from {full_module_path} overrides existing cleaning"
                                    )
                                
                                # Register the cleaning
                                cls._cleaners[cleaning_name] = attr
                                print(
                                    f"Successfully loaded plugin cleaning: "
                                    f"{cleaning_name} -> {attr.__name__}"
                                )
                            else:
                                print(
                                    f"Warning: Cleaning class {attr.__name__} in {full_module_path} "
                                    f"lacks 'name' attribute. Skipping registration."
                                )
                                
                except ImportError as e:
                    print(f"Error importing plugin module {module_name}: {e}")
                except Exception as e:
                    print(f"Error loading plugin from {module_file.name}: {e}")
                    
        except Exception as e:
            print(f"Unexpected error during plugin loading: {e}")