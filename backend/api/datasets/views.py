from django.views import View
from django.http import JsonResponse
from api.storage import list_datasets, get_dataset
import json
from api.storage import get_dataset
class DatasetListView(View):
    """Returns a list of available datasets"""
    def get(self, request):
        return JsonResponse({"datasets": list_datasets()})

class DatasetDetailView(View):
    """Fetches a dataset by name and ensures response is proper JSON"""
    def get(self, request, dataset_name):
        dataset = get_dataset(dataset_name)
        if dataset is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        try:
            dataset_json = dataset.to_dict(orient="records")  # ✅ Ensures correct JSON format
            print(type(dataset_json))
            return JsonResponse({"data": dataset_json}, safe=False)  # ✅ Prevents Django from converting it into a string
        except Exception as e:
            return JsonResponse({"error": "JSON serialization failed", "details": str(e)}, status=500)
