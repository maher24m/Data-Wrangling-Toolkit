class CleaningProcessorFactory:
    """Factory for creating cleaning processors dynamically with lazy loading"""
    _processors = None

    @classmethod
    def _initialize_processors(cls):
        """Lazy initialization to load processors only when first accessed"""
        if cls._processors is None:
            from api.datacleaning.registry import load_processors  # Prevents unnecessary execution
            cls._processors = load_processors()

    @classmethod
    def get_processor(cls, operation_type):
        """Retrieve a cleaning processor based on operation type, ensuring processors are loaded first"""
        cls._initialize_processors()
        if operation_type not in cls._processors:
            raise ValueError(f"Unsupported cleaning operation: {operation_type}")
        return cls._processors[operation_type]()

    @classmethod
    def list_processors(cls):
        """Returns a list of available cleaning operations"""
        cls._initialize_processors()
        return list(cls._processors.keys()) 