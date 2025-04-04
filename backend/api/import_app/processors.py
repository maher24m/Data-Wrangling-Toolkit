import pandas as pd
import json
import xml.etree.ElementTree as ET

class FileProcessor:
    """Base class for all file processors"""
    def process(self, file):
        raise NotImplementedError("Subclasses must implement this method")

# 🔥 Default Processors
class CSVProcessor(FileProcessor):
    def process(self, file):
        return pd.read_csv(file)

class ExcelProcessor(FileProcessor):
    def process(self, file):
        return pd.read_excel(file)

class JSONProcessor(FileProcessor):
    def process(self, file):
        data = json.load(file)
        return pd.DataFrame(data)

class XMLProcessor(FileProcessor):
    def process(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        data = [{child.tag: child.text for child in item} for item in root]
        return pd.DataFrame(data)

class ParquetProcessor(FileProcessor):
    def process(self, file):
        return pd.read_parquet(file)
