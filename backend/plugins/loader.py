import importlib
import os
import pkgutil

def load_plugins(plugin_folder, factory_class):
    """Dynamically loads plugins from a given folder and registers them."""
    package_dir = os.path.join(os.path.dirname(__file__), plugin_folder)
    
    for _, module_name, _ in pkgutil.iter_modules([package_dir]):
        module = importlib.import_module(f"plugins.{plugin_folder}.{module_name}")

        # Auto-register processors if they inherit from the base class
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and hasattr(attr, "apply"):  # Ensure it's a valid processor
                factory_class.register_processor(module_name, attr)
