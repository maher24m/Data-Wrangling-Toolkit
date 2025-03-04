from django.views import View
from django.http import JsonResponse
from datasets.manager import DatasetManager

class DatasetListView(View):
    """Returns a list of available datasets"""
    def get(self, request):
        datasets = DatasetManager.list_datasets()
        active_dataset = DatasetManager.get_active_dataset()
        return JsonResponse({
            "datasets": datasets,
            "active_dataset": active_dataset
        })

class DatasetDetailView(View):
    """Fetches the currently active dataset"""
    def get(self, request):
        dataset = DatasetManager.get_active_dataset()
        if dataset is None:
            return JsonResponse({"error": "No active dataset selected"}, status=404)
        return JsonResponse({"data": dataset})

    def post(self, request):
        """Set a dataset as active"""
        dataset_name = request.POST.get("dataset_name")
        if not dataset_name:
            return JsonResponse({"error": "Dataset name required"}, status=400)

        dataset = DatasetManager.get_dataset(dataset_name)
        if dataset is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        DatasetManager.set_active_dataset(dataset_name)
        return JsonResponse({"success": True, "active_dataset": dataset_name})
