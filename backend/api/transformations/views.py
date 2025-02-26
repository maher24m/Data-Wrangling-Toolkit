from django.views import View
from django.http import JsonResponse
import pandas as pd
from api.storage import get_dataset, save_dataset
import numpy as np

class ApplyTransformationView(View):
    """Applies transformations to a dataset"""
    def post(self, request, dataset_name):
        dataset = get_dataset(dataset_name)
        if dataset is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        column = request.POST.get("column")
        transformation = request.POST.get("transformation")

        df = pd.DataFrame(dataset)

        if column not in df.columns:
            return JsonResponse({"error": "Invalid column name"}, status=400)

        if transformation == "normalize":
            df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
        elif transformation == "log":
            df[column] = df[column].apply(lambda x: 0 if x <= 0 else np.log(x))
        else:
            return JsonResponse({"error": "Unsupported transformation"}, status=400)

        save_dataset(dataset_name, df.to_dict(orient="records"))
        return JsonResponse({"success": True, "message": f"Applied {transformation} to {column}"})
