import importlib
from pathlib import Path

class FileExporterFactory:
    """Factory for creating file exporters dynamically."""
    _exporters = None

    @classmethod
    def _initialize_exporters(cls):
        """Lazy initialization to load exporters only when first accessed."""
        if cls._exporters is None:
            cls._exporters = {}
            cls._register_default_exporters()  # Register default exporters
            cls._load_plugins("api.plugins")   # Load user-defined plugins (optional)

    @classmethod
    def _register_default_exporters(cls):
        """Register default exporters with error handling."""
        default_exporters = {
            "csv": "api.export_app.exporters.CSVExporter",
            "json": "api.export_app.exporters.JSONExporter",
            "excel": "api.export_app.exporters.ExcelExporter",
            "xml": "api.export_app.exporters.XMLExporter",
            "parquet": "api.export_app.exporters.ParquetExporter",
        }

        for format_type, exporter_class_path in default_exporters.items():
            try:
                # Split the module and class name
                module_name, class_name = exporter_class_path.rsplit(".", 1)
                
                # Import the module dynamically
                module = importlib.import_module(module_name)
                
                # Get the exporter class from the module
                exporter_class = getattr(module, class_name)
                
                # Register the exporter
                cls._exporters[format_type] = exporter_class
                
                print(f"Successfully registered exporter: {format_type} -> {exporter_class.__name__}")
            except Exception as e:
                print(f"Error registering exporter for format '{format_type}': {e}")

    @classmethod
    def _load_plugins(cls, plugin_dir):
        """Dynamically load plugins from a directory."""
        try:
            from api.export_app.exporters import Exporter  # Import the base class
            
            plugin_path = Path(plugin_dir)
            for module_file in plugin_path.glob("*.py"):
                if module_file.name != "__init__.py":
                    try:
                        module_name = module_file.stem
                        module = importlib.import_module(f"{plugin_dir}.{module_name}")
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if (
                                isinstance(attr, type)
                                and issubclass(attr, Exporter)
                                and attr != Exporter
                            ):
                                format_type = getattr(attr, "format_type", None)
                                if format_type:
                                    cls._exporters[format_type] = attr
                                    print(f"Successfully loaded plugin exporter: {format_type} -> {attr.__name__}")
                    except Exception as e:
                        print(f"Error loading plugin module {module_name}: {e}")
        except ImportError:
            print("Warning: Exporter base class not found. Plugin loading skipped.")
        except Exception as e:
            print(f"Unexpected error during plugin loading: {e}")

    @classmethod
    def register_exporter(cls, format_type, exporter_class):
        """Register a new exporter manually."""
        cls._initialize_exporters()
        cls._exporters[format_type] = exporter_class

    @classmethod
    def get_exporter(cls, format_type):
        """Retrieve an exporter based on format type."""
        cls._initialize_exporters()
        exporter_class = cls._exporters.get(format_type)
        if not exporter_class:
            raise ValueError(f"No exporter found for format: {format_type}")
        return exporter_class()

    @classmethod
    def list_exporters(cls):
        """Returns a list of available export formats."""
        cls._initialize_exporters()
        return list(cls._exporters.keys())