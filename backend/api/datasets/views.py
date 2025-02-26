from django.views import View
from django.http import JsonResponse
from api.storage import list_datasets, get_dataset

class DatasetListView(View):
    """Returns a list of available datasets"""
    def get(self, request):
        return JsonResponse({"datasets": list_datasets()})

class DatasetDetailView(View):
    """Fetches a dataset by name"""
    def get(self, request, dataset_name):
        dataset = get_dataset(dataset_name)
        if dataset is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        return JsonResponse({"data": dataset})
