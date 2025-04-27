import importlib
from pathlib import Path

class DataCleaningFactory:
    """Factory for creating data-cleaning operations dynamically."""
    _processors = None

    @classmethod
    def _initialize_processors(cls):
        """Lazy init: load processors only once, on first access."""
        if cls._processors is None:
            cls._processors = {}
            cls._register_default_processors()
            cls._load_plugins("api.plugins.cleaning")

    @classmethod
    def _register_default_processors(cls):
        """Register all the built-in cleaning operations."""
        default_processors = {
            "remove_duplicates":      "api.datacleaning.processor.RemoveDuplicatesProcessor",
            "fill_missing_mean":      "api.datacleaning.processor.FillMissingMeanProcessor",
            "fill_missing_median":    "api.datacleaning.processor.FillMissingMedianProcessor",
            "fill_missing_mode":      "api.datacleaning.processor.FillMissingModeProcessor",
            "replace_missing_value":  "api.datacleaning.processor.ReplaceMissingValueProcessor",
            "remove_missing_data":    "api.datacleaning.processor.RemoveMissingDataProcessor",
            "detect_outliers":        "api.datacleaning.processor.DetectOutliersProcessor",
            "replace_outliers":       "api.datacleaning.processor.ReplaceOutliersProcessor",
            "standardize_format":     "api.datacleaning.processor.StandardizeFormatProcessor",
            "cluster_similar":"api.datacleaning.processor.ClusterSimilarValuesProcessor",
        }

        for op_name, class_path in default_processors.items():
            try:
                module_name, class_name = class_path.rsplit(".", 1)
                module = importlib.import_module(module_name)
                cleaner_cls = getattr(module, class_name)
                cls._processors[op_name] = cleaner_cls
                print(f"Registered cleaner: {op_name} -> {class_name}")
            except Exception as e:
                print(f"Error registering cleaner '{op_name}': {e}")

    @classmethod
    def _load_plugins(cls, plugin_dir: str):
        """Optionally discover user-provided processors in a plugin folder."""
        from api.datacleaning.processor import DataCleaningProcessor
        try:
            path = Path(plugin_dir)
            for file in path.glob("*.py"):
                if file.name == "__init__.py":
                    continue
                module_name = file.stem
                try:
                    module = importlib.import_module(f"{plugin_dir}.{module_name}")
                    for attr in dir(module):
                        obj = getattr(module, attr)
                        if (
                            isinstance(obj, type)
                            and issubclass(obj, DataCleaningProcessor)
                            and obj is not DataCleaningProcessor
                        ):
                            op = getattr(obj, "operation_name", None)
                            if op:
                                cls._processors[op] = obj
                                print(f"Loaded plugin cleaner: {op} -> {obj.__name__}")
                except Exception as e:
                    print(f"Error loading plugin '{module_name}': {e}")
        except Exception:
            print("Plugin directory not found or error importing CleaningProcessor; skipping plugins.")

    @classmethod
    def register_processor(cls, operation_name: str, cleaner_cls: type):
        """Manually register a new cleaner."""
        cls._initialize_processors()
        cls._processors[operation_name] = cleaner_cls

    @classmethod
    def get_processor(cls, operation_name: str):
        """Retrieve an instance of the cleaner for the given operation."""
        cls._initialize_processors()
        cleaner_cls = cls._processors.get(operation_name)
        if not cleaner_cls:
            raise ValueError(f"No data-cleaner found for operation: {operation_name}")
        return cleaner_cls()

    @classmethod
    def list_processors(cls):
        """List all available cleaning operations."""
        cls._initialize_processors()
        return list(cls._processors.keys())
