# backend/api/datacleaning/factory.py
import importlib
from pathlib import Path
# --- FIX: Import the renamed base processor class ---
from api.datacleaning.processor import DataCleaningProcessor

class DataCleaningFactory:
    """Factory for creating data-cleaning operations dynamically."""
    _processors = None

    @classmethod
    def _initialize_processors(cls):
        """Lazy init: load processors only once, on first access."""
        if cls._processors is None:
            cls._processors = {}
            cls._register_default_processors()
            # --- FIX: Adjust plugin path if needed, convert to Path object ---
            # Assuming api/plugins/cleaning relative to project root might need adjustment
            # Let's assume the string 'api.plugins.cleaning' correctly points to the directory
            # structure relative to where Python runs.
            base_path = Path(__file__).resolve().parent.parent.parent # Adjust based on your project structure
            plugin_path = base_path / "api" / "plugins" / "cleaning"
            # Convert path to module import format if needed, or keep using the string?
            # The original code used the string 'api.plugins.cleaning' for importlib,
            # and Path(plugin_dir) for file iteration. Let's stick to that pattern.
            cls._load_plugins("api.plugins.cleaning")


    @classmethod
    def _register_default_processors(cls):
        """Register all the built-in cleaning operations."""
        # --- FIX: Use simplified keys and map to appropriate processors ---
        # Use more general keys that match the API intent and tests.
        # Map operations to the corresponding processor class paths.
        default_processors = {
            # MissingValuesCleaner handles mean, median, mode, constant, remove
            "missing_values":    "api.datacleaning.processor.MissingValuesCleaner",
            "remove_duplicates": "api.datacleaning.processor.RemoveDuplicatesCleaner",
            "detect_outliers":   "api.datacleaning.processor.DetectOutliersCleaner",
            "replace_outliers":  "api.datacleaning.processor.ReplaceOutliersCleaner",
            "standardize_format":"api.datacleaning.processor.StandardizeFormatCleaner",
            "cluster_similar":   "api.datacleaning.processor.ClusterSimilarCleaner", # Corrected class name if changed
            # Add aliases if you want to keep old names temporarily, e.g.:
                }

        # Store the processor classes directly
        cls._processors = {}
        for op_name, class_path in default_processors.items():
            try:
                module_name, class_name = class_path.rsplit(".", 1)
                module = importlib.import_module(module_name)
                cleaner_cls = getattr(module, class_name)
                cls._processors[op_name] = cleaner_cls
                # print(f"Registered default processor: {op_name} -> {class_name}") # Optional: Keep for debug
            except ImportError as e:
                print(f"Error importing module for processor '{op_name}': {e}")
            except AttributeError as e:
                print(f"Error finding class for processor '{op_name}': {e}")
            except Exception as e:
                print(f"Unexpected error registering processor '{op_name}': {e}")

    @classmethod
    def _load_plugins(cls, plugin_module_path: str):
        """Optionally discover user-provided processors in a plugin folder."""
        # --- FIX: Use the renamed DataCleaningProcessor ---
        # Note: This still relies on the plugin classes having an 'operation_name' attribute.
        try:
            # Find the directory corresponding to the module path
            plugin_spec = importlib.util.find_spec(plugin_module_path)
            if plugin_spec is None or plugin_spec.origin is None or not Path(plugin_spec.origin).parent.is_dir():
                 print(f"Plugin directory for '{plugin_module_path}' not found. Skipping plugins.")
                 return

            plugin_dir = Path(plugin_spec.origin).parent

            for file in plugin_dir.glob("*.py"):
                if file.name == "__init__.py" or not file.is_file():
                    continue

                module_name_short = file.stem
                full_module_name = f"{plugin_module_path}.{module_name_short}"
                try:
                    module = importlib.import_module(full_module_name)
                    for attr_name in dir(module):
                        potential_cls = getattr(module, attr_name)
                        # Check if it's a class, a subclass of DataCleaningProcessor,
                        # not DataCleaningProcessor itself, and has an operation_name
                        if (
                            isinstance(potential_cls, type) and
                            issubclass(potential_cls, DataCleaningProcessor) and
                            potential_cls is not DataCleaningProcessor
                        ):
                            op_name = getattr(potential_cls, "operation_name", None)
                            if op_name:
                                if op_name in cls._processors:
                                     print(f"Warning: Plugin '{op_name}' from {full_module_name} overrides existing processor.")
                                cls._processors[op_name] = potential_cls
                                # print(f"Loaded plugin processor: {op_name} -> {potential_cls.__name__}") # Optional: Keep for debug
                            # else: # Optional: Warn about processors without operation_name
                            #    print(f"Warning: Plugin class {potential_cls.__name__} in {full_module_name} lacks 'operation_name' attribute.")
                except ImportError as e:
                    print(f"Error importing plugin module '{full_module_name}': {e}")
                except Exception as e:
                    print(f"Error loading plugin from '{file.name}': {e}")
        except ModuleNotFoundError:
             print(f"Plugin module path '{plugin_module_path}' not found. Skipping plugins.")
        except Exception as e:
            print(f"Error accessing plugin directory '{plugin_module_path}': {e}. Skipping plugins.")


    @classmethod
    def register_processor(cls, operation_name: str, cleaner_cls: type):
        """Manually register a new cleaner."""
        cls._initialize_processors() # Ensure dict exists
        if not issubclass(cleaner_cls, DataCleaningProcessor):
             raise TypeError(f"Processor class must inherit from DataCleaningProcessor: {cleaner_cls.__name__}")
        if operation_name in cls._processors:
             print(f"Warning: Registering processor '{operation_name}' overrides existing processor.")
        cls._processors[operation_name] = cleaner_cls

    @classmethod
    def get_processor(cls, operation_name: str) -> DataCleaningProcessor:
        """Retrieve an instance of the cleaner for the given operation."""
        cls._initialize_processors()
        cleaner_cls = cls._processors.get(operation_name)
        if not cleaner_cls:
            raise ValueError(f"No data-cleaner processor found for operation type: '{operation_name}'")
        # Return an instance
        return cleaner_cls()

    @classmethod
    def list_processors(cls) -> list[str]:
        """List all available cleaning operation types."""
        cls._initialize_processors()
        return sorted(list(cls._processors.keys()))