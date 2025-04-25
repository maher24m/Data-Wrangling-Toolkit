import pandas as pd
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from .factory import FileProcessorFactory

class FileProcessor:
    """
    Facade: picks the right concrete processor via the factory
    and delegates the process call.
    """
    def process(self, file):
        # Determine format key from file extension (e.g. 'csv', 'json', etc.)
        fmt = Path(file).suffix.lstrip('.').lower()
        print(fmt)
        if not fmt:
            raise ValueError(f"Cannot infer format from path: {file}")

        processor = FileProcessorFactory.get_processor(fmt)
        return processor.process(file)


# Default Processors
class CSVProcessor(FileProcessor):
    def process(self, file):
        return pd.read_csv(file)

class ExcelProcessor(FileProcessor):
    def process(self, file):
        return pd.read_excel(file)

class JSONProcessor(FileProcessor):
    def process(self, file):
        return pd.read_json(file)

class XMLProcessor(FileProcessor):
    def process(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        data = [{child.tag: child.text for child in item} for item in root]
        return pd.DataFrame(data)

class ParquetProcessor(FileProcessor):
    def process(self, file):
        return pd.read_parquet(file)
