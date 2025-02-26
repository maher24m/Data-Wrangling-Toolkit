from django.views import View
from django.http import JsonResponse
import pandas as pd
from api.storage import get_dataset

class DataAnalysisView(View):
    """Performs data analysis on a dataset"""
    def get(self, request, dataset_name):
        dataset = get_dataset(dataset_name)
        if dataset is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        df = pd.DataFrame(dataset)
        summary = df.describe().to_dict()

        return JsonResponse({"summary": summary})
