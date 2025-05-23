# api/export_app/exporters.py

import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path


class Exporter:
    """
    Facade: picks the right concrete exporter via the factory
    and delegates the export call.
    """
    
    def export(self, data, file_path):
        raise RuntimeError(
            "FileProcessor is deprecated and should not be used. "
            "Please switch to the new import pipeline."
        )


class CSVExporter(Exporter):
    def export(self, data, file_path):
        df = pd.DataFrame(data)
        return df.to_csv(file_path, index=False)

class JSONExporter(Exporter):
    def export(self, data, file_path):
        df = pd.DataFrame(data)
        return df.to_json(file_path, orient="records", lines=True)

class ExcelExporter(Exporter): #FAILED
    def export(self, data, file_path):
        df = pd.DataFrame(data)
        return df.to_excel(file_path, index=False)

class XMLExporter(Exporter):
    def export(self, data, file_path):
        df = pd.DataFrame(data)
        
        # Create the root element
        root = ET.Element('root')
        
        # Convert DataFrame rows to XML
        for _, row in df.iterrows():
            item = ET.SubElement(root, 'item')
            for col_name, value in row.items():
                child = ET.SubElement(item, str(col_name))
                child.text = str(value)
        
        # Create XML tree and save
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        return True

class ParquetExporter(Exporter):
    def export(self, data, file_path):
        df = pd.DataFrame(data)
        return df.to_parquet(file_path, index=False)
    
#we can make it export whatever in the storage directory
