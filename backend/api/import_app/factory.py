from import_app.processor import FileProcessor

class FileProcessorFactory:
    """Factory for creating file processors dynamically"""
    _processors = {}

    @staticmethod
    def register_processor(file_type, processor_class):
        """Registers a new file processor dynamically"""
        if not issubclass(processor_class, FileProcessor):
            raise TypeError("Processor must inherit from FileProcessor")
        FileProcessorFactory._processors[file_type] = processor_class

    @staticmethod
    def get_processor(file_type):
        """Retrieves a file processor based on file type"""
        if file_type not in FileProcessorFactory._processors:
            raise ValueError(f"Unsupported file format: {file_type}")
        return FileProcessorFactory._processors[file_type]()
