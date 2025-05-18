from typing import Dict, Type, Any
from .base import BaseTransformation
from .transformations.normalize import NormalizeTransformation
from .transformations.log import LogTransformation
from .transformations.square_root import SquareRootTransformation

class TransformationFactory:
    """Factory for managing transformations"""
    
    _transformations: Dict[str, Type[BaseTransformation]] = {
        'normalize': NormalizeTransformation,
        'log': LogTransformation,
        'square_root': SquareRootTransformation
    }
    
    @classmethod
    def get_transformation(cls, name: str) -> BaseTransformation:
        """Get a transformation by name"""
        if name not in cls._transformations:
            raise ValueError(f"Transformation {name} not found")
        return cls._transformations[name]()
    
    @classmethod
    def list_transformations(cls) -> Dict[str, Dict[str, Any]]:
        """List all available transformations with their descriptions and parameters"""
        return {
            name: {
                'description': transformation().description,
                'parameters': transformation().parameters
            }
            for name, transformation in cls._transformations.items()
        }
