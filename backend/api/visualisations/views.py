from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import pandas as pd
import json
from api.storage import get_dataset
from api.visualisations.factory import VisualizationFactory

@method_decorator(csrf_exempt, name="dispatch")
class VisualizationView(View):
    """Generates visualization data for a dataset"""
    
    def get(self, request, dataset_name, chart_type):
        """
        Generate visualization data for a dataset
        
        Args:
            request: HTTP request
            dataset_name: Name of the dataset to visualize
            chart_type: Type of chart to generate
            
        Returns:
            JsonResponse: Visualization data
        """
        dataset = get_dataset(dataset_name)
        if dataset is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        df = pd.DataFrame(dataset)
        
        try:
            # Get the appropriate visualizer from the factory
            visualizer = VisualizationFactory.get_visualizer(chart_type)
            
            # Get query parameters for visualization options
            params = {}
            for key, value in request.GET.items():
                # Convert string values to appropriate types
                if value.lower() == 'true':
                    params[key] = True
                elif value.lower() == 'false':
                    params[key] = False
                elif value.isdigit():
                    params[key] = int(value)
                elif value.replace('.', '', 1).isdigit() and value.count('.') <= 1:
                    params[key] = float(value)
                else:
                    params[key] = value
            
            # Generate visualization data
            visualization_data = visualizer.visualize(df, **params)
            
            return JsonResponse(visualization_data)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error generating visualization: {str(e)}"}, status=500)

@method_decorator(csrf_exempt, name="dispatch")
class AvailableVisualizationsView(View):
    """Returns a list of available visualization types"""
    
    def get(self, request):
        """
        Get a list of available visualization types
        
        Args:
            request: HTTP request
            
        Returns:
            JsonResponse: List of available visualization types
        """
        try:
            visualizers = VisualizationFactory.list_visualizers()
            return JsonResponse({"visualizations": visualizers})
        except Exception as e:
            return JsonResponse({"error": f"Error listing visualizations: {str(e)}"}, status=500)
