from transformations.processor import NormalizeProcessor, LogProcessor, SquareRootProcessor
from transformations.factory import TransformationProcessorFactory

# 🔥 Register default transformations
TransformationProcessorFactory.register_processor("normalize", NormalizeProcessor)
TransformationProcessorFactory.register_processor("log", LogProcessor)
TransformationProcessorFactory.register_processor("square_root", SquareRootProcessor)
