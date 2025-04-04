from api.transformations.processor import NormalizeProcessor, LogProcessor, SquareRootProcessor
from backend.plugins.base import load_plugins  # 🔥 Load transformation plugins dynamically

def load_processors():
    """Loads and returns available transformation processors in a dictionary (Lazy Initialization)"""
    processors = {}

    # 🔥 Register default transformation processors
    processors["normalize"] = NormalizeProcessor
    processors["log"] = LogProcessor
    processors["square_root"] = SquareRootProcessor

    # 🔥 Load user-defined transformation plugins from `plugins/transformations/`
    load_plugins("transformations", processors)

    return processors
