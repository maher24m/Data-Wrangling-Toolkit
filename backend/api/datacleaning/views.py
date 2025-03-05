from django.views import View
from django.http import JsonResponse
import pandas as pd
from api.storage import get_dataset, save_dataset

class DataCleaningView(View):
    """Handles dataset cleaning operations"""
    def post(self, request, dataset_name):
        dataset = get_dataset(dataset_name)
        if dataset is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        operation = request.POST.get("operation")
        df = pd.DataFrame(dataset)

        if operation == "remove_nulls":
            df = df.dropna()
        elif operation == "remove_duplicates":
            df = df.drop_duplicates()
        else:
            return JsonResponse({"error": "Unsupported cleaning operation"}, status=400)

        save_dataset(dataset_name, df.to_dict(orient="records"))
        return JsonResponse({"success": True, "message": f"Performed {operation}"})
