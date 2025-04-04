# api/plugins/base.py

from abc import ABC, abstractmethod

class FileProcessorPlugin(ABC):
    """Base class for file processor plugins."""

    @abstractmethod
    def process(self, file):
        """Process the uploaded file."""
        pass