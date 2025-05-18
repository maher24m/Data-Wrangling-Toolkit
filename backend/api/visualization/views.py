from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .factory import VisualizationFactory
from ..datasets.manager import get_dataset

@method_decorator(csrf_exempt, name="dispatch")
class ApplyVisualizationView(View):
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
                visualization_name = body.get('visualization')
                parameters = body.get('parameters', {})
            except json.JSONDecodeError:
                return JsonResponse(
                    {"error": "Invalid JSON payload"},
                    status=400
                )
            
            if not visualization_name:
                return JsonResponse(
                    {"error": "Visualization name is required"},
                    status=400
                )
            
            # Get and apply visualization
            visualization = VisualizationFactory.get_visualization(visualization_name)
            results = visualization.visualize(df, **parameters)
            
            return JsonResponse({
                "message": "Visualization created successfully",
                "dataset": dataset_name,
                "visualization": visualization_name,
                "figure": results
            })
            
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": "Failed to create visualization", "details": str(e)},
                status=500
            )

@method_decorator(csrf_exempt, name="dispatch")
class AvailableVisualizationsView(View):
    def get(self, request):
        """Returns a list of available visualizations"""
        try:
            visualizations = VisualizationFactory.list_visualizations()
            return JsonResponse({
                "visualizations": visualizations
            })
        except Exception as e:
            return JsonResponse(
                {"error": "Failed to list visualizations", "details": str(e)},
                status=500
            ) 