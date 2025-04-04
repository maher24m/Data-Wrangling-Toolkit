# api/factory.py

import importlib
from pathlib import Path

class FileProcessorFactory:
    """Factory for creating file processors dynamically."""
    _processors = None
    _mime_mapping = None

    @classmethod
    def _initialize_processors(cls):
        """Lazy initialization to load processors only when first accessed."""
        if cls._processors is None:
            cls._processors = {}
            cls._mime_mapping = {}
            cls._register_default_processors()  # Register default processors
            cls._load_plugins("api.plugins")   # Load user-defined plugins (optional)

    @classmethod
    def _register_default_processors(cls):
        """Register default processors with error handling."""
        default_processors = {
            "text/csv": "api.import_app.processors.CSVProcessor",
            "application/vnd.ms-excel": "api.import_app.processors.ExcelProcessor",
            "application/json": "api.import_app.processors.JSONProcessor",
            "application/xml": "api.import_app.processors.XMLProcessor",
            "application/parquet": "api.import_app.processors.ParquetProcessor",
        }

        for file_type, processor_class_path in default_processors.items():
            try:
                # Split the module and class name
                module_name, class_name = processor_class_path.rsplit(".", 1)
                
                # Import the module dynamically
                module = importlib.import_module(module_name)
                
                # Get the processor class from the module
                processor_class = getattr(module, class_name)
                
                # Register the processor
                cls._processors[file_type] = processor_class
                cls._mime_mapping[file_type] = class_name.replace("Processor", "")
                
                print(f"Successfully registered: {file_type} -> {processor_class.__name__}")  # Debug output
            except ModuleNotFoundError as e:
                print(f"Error: Module '{module_name}' not found for file type '{file_type}'. Skipping registration.")
            except AttributeError as e:
                print(f"Error: Class '{class_name}' not found in module '{module_name}' for file type '{file_type}'. Skipping registration.")
            except Exception as e:
                print(f"Unexpected error while registering processor for file type '{file_type}': {e}. Skipping registration.")

    @classmethod
    def _load_plugins(cls, plugin_dir):
        """Dynamically load plugins from a directory."""
        plugin_path = Path(plugin_dir)
        for module_file in plugin_path.glob("*.py"):
            if module_file.name != "__init__.py":
                module_name = module_file.stem
                module = importlib.import_module(f"{plugin_dir}.{module_name}")
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, FileProcessor)
                        and attr != FileProcessor
                    ):
                        file_type = getattr(attr, "file_type", None)
                        if file_type:
                            cls._processors[file_type] = attr
                            cls._mime_mapping[file_type] = getattr(
                                attr, "human_readable_name", file_type
                            )

    @classmethod
    def get_processor(cls, file_type):
        """Retrieve a processor based on MIME type."""
        cls._initialize_processors()
        if file_type not in cls._processors:
            raise ValueError(f"Unsupported file format: {file_type}")
        return cls._processors[file_type]()

    @classmethod
    def list_processors(cls):
        """Returns a list of available file types in human-readable format."""
        cls._initialize_processors()
        return list(cls._mime_mapping.values())