from django.views import View
from django.http import JsonResponse
import pandas as pd
from api.storage import get_dataset

class VisualizationView(View):
    """Generates visualization data for a dataset"""
    def get(self, request, dataset_name, chart_type):
        dataset = get_dataset(dataset_name)
        if dataset is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        df = pd.DataFrame(dataset)

        if chart_type == "bar":
            chart_data = df.value_counts().to_dict()
        elif chart_type == "scatter":
            chart_data = df.corr().to_dict()
        else:
            return JsonResponse({"error": "Unsupported chart type"}, status=400)

        return JsonResponse({"chart_data": chart_data})
