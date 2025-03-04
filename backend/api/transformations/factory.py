class TransformationProcessorFactory:
    """Factory for creating transformation processors dynamically."""
    _processors = {}

    @staticmethod
    def register_processor(transformation_type, processor_class):
        """Registers a new transformation processor dynamically."""
        if not issubclass(processor_class, TransformationProcessor):
            raise TypeError("Processor must inherit from TransformationProcessor")
        TransformationProcessorFactory._processors[transformation_type] = processor_class

    @staticmethod
    def get_processor(transformation_type):
        """Retrieves a transformation processor based on transformation type."""
        if transformation_type not in TransformationProcessorFactory._processors:
            raise ValueError(f"Unsupported transformation type: {transformation_type}")
        return TransformationProcessorFactory._processors[transformation_type]()
