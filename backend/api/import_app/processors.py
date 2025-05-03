import pandas as pd
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from .factory import FileProcessorFactory

# api/processing/file_processor.py

class FileProcessor:
    """
    Stub facade: this should not be used. Always errors out.
    """
    def process(self, file):
        raise RuntimeError(
            "FileProcessor is deprecated and should not be used. "
            "Please switch to the new import pipeline."
        )

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
