from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .factory import TransformationFactory
from ..datasets.manager import get_dataset, save_dataset

class ApplyTransformationView(APIView):
    def post(self, request, dataset_name):
        try:
            # Get the dataset
            df = get_dataset(dataset_name)
            if df is None:
                return Response(
                    {"error": f"Dataset '{dataset_name}' not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get transformation parameters
            transformation_name = request.data.get('transformation')
            parameters = request.data.get('parameters', {})
            
            if not transformation_name:
                return Response(
                    {"error": "Transformation name is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get and apply transformation
            transformation = TransformationFactory.get_transformation(transformation_name)
            df = transformation.transform(df, **parameters)
            
            # Save transformed dataset
            save_dataset(dataset_name, df)
            
            return Response({
                "message": "Transformation applied successfully",
                "dataset": dataset_name
            })
            
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Error applying transformation: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AvailableTransformationsView(APIView):
    def get(self, request):
        """List all available transformations"""
        transformations = TransformationFactory.list_transformations()
        return Response(transformations)