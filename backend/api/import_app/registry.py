from api.import_app.processor import FileProcessor, CSVProcessor
from api.import_app.factory import FileProcessorFactory

FileProcessorFactory.register_processor("text/csv", CSVProcessor)