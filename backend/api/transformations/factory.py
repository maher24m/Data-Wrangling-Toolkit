class TransformationProcessorFactory:
    """Factory for creating transformation processors dynamically with lazy loading"""
    _processors = None  # Use None to delay initialization

    @classmethod
    def _initialize_processors(cls):
        """Lazy initialization to load processors only when first accessed"""
        if cls._processors is None:
            from api.transformations.registry import load_processors  # Prevents unnecessary execution
            cls._processors = load_processors()

    @classmethod
    def get_processor(cls, transformation_type):
        """Retrieve a transformation processor based on type, ensuring processors are loaded first"""
        cls._initialize_processors()
        if transformation_type not in cls._processors:
            raise ValueError(f"Unsupported transformation type: {transformation_type}")
        return cls._processors[transformation_type]()

    @classmethod
    def list_processors(cls):
        """Returns a list of available transformations"""
        cls._initialize_processors()
        return list(cls._processors.keys())
