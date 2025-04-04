# api/export_app/exporters.py

import pandas as pd
import xml.etree.ElementTree as ET
import json

class Exporter:
    """Base class for all data exporters"""
    def export(self, data, file_path):
        raise NotImplementedError("Subclasses must implement this method")

class CSVExporter(Exporter):
    def export(self, data, file_path):
        df = pd.DataFrame(data)
        return df.to_csv(file_path, index=False)

class JSONExporter(Exporter):
    def export(self, data, file_path):
        df = pd.DataFrame(data)
        return df.to_json(file_path, orient="records", lines=True)

class ExcelExporter(Exporter):
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
