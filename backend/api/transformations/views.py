# from rest_framework.views import APIView
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .factory import TransformationFactory
from ..datasets.manager import get_dataset, save_dataset

@method_decorator(csrf_exempt, name="dispatch")
class ApplyTransformationView(View):
    def post(self, request, dataset_name):
        try:
            # Get the dataset
            df = get_dataset(dataset_name)
            if df is None:
                return JsonResponse(
                    {"error": f"Dataset '{dataset_name}' not found"},
                    status=404
                )
            
            # Parse request body
            try:
                body = json.loads(request.body)
                transformation_name = body.get('transformation')
                parameters = body.get('parameters', {})
            except json.JSONDecodeError:
                return JsonResponse(
                    {"error": "Invalid JSON payload"},
                    status=400
                )
            
            if not transformation_name:
                return JsonResponse(
                    {"error": "Transformation name is required"},
                    status=400
                )
            
            # Get and apply transformation
            transformation = TransformationFactory.get_transformation(transformation_name)
            df = transformation.transform(df, **parameters)
            
            # Save transformed dataset
            save_dataset(dataset_name, df)
            
            return JsonResponse({
                "message": "Transformation applied successfully",
                "dataset": dataset_name,
                "rows": len(df),
                "columns": len(df.columns)
            })
            
        except ValueError as e:
            return JsonResponse(
                {"error": str(e)},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {"error": f"Error applying transformation: {str(e)}"},
                status=500
            )

@method_decorator(csrf_exempt, name="dispatch")
class AvailableTransformationsView(View):
    def get(self, request):
        """List all available transformations"""
        try:
            transformations = TransformationFactory.list_transformations()
            return JsonResponse({"transformations": transformations})
        except Exception as e:
            return JsonResponse(
                {"error": f"Error retrieving transformations: {str(e)}"},
                status=500
            )