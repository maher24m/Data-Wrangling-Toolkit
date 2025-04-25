from api.datacleaning.processor import (
    RemoveNullsProcessor, 
    RemoveDuplicatesProcessor,
    FillNullsProcessor,
    ReplaceValuesProcessor
)
import importlib
from pathlib import Path

def load_processors():
    """Loads and returns available cleaning processors in a dictionary (Lazy Initialization)"""
    processors = {}

    # Register default cleaning processors
    processors["remove_nulls"] = RemoveNullsProcessor
    processors["remove_duplicates"] = RemoveDuplicatesProcessor
    processors["fill_nulls"] = FillNullsProcessor
    processors["replace_values"] = ReplaceValuesProcessor

    # Load user-defined cleaning plugins from `plugins/cleaning/`
    try:
        plugin_path = Path("api/plugins/cleaning")
        if plugin_path.exists():
            for module_file in plugin_path.glob("*.py"):
                if module_file.name != "__init__.py":
                    try:
                        module_name = module_file.stem
                        module = importlib.import_module(f"api.plugins.cleaning.{module_name}")
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if (
                                isinstance(attr, type)
                                and issubclass(attr, CleaningProcessor)
                                and attr != CleaningProcessor
                            ):
                                operation_type = getattr(attr, "operation_type", None)
                                if operation_type:
                                    processors[operation_type] = attr
                                    print(f"Successfully loaded cleaning plugin: {operation_type} -> {attr.__name__}")
                    except Exception as e:
                        print(f"Error loading cleaning plugin module {module_name}: {e}")
    except Exception as e:
        print(f"Unexpected error during cleaning plugin loading: {e}")

    return processors 