from django.views import View
from django.http import JsonResponse
import pandas as pd
from api.storage import save_dataset

class FileUploadView(View):
    """Uploads a dataset file and stores it."""
    def post(self, request):
        if "file" not in request.FILES or "dataset_name" not in request.POST:
            return JsonResponse({"error": "File and dataset name required"}, status=400)

        dataset_name = request.POST["dataset_name"]
        uploaded_file = request.FILES["file"]

        # Process CSV or Excel
        if uploaded_file.content_type == "text/csv":
            df = pd.read_csv(uploaded_file)
        elif "spreadsheet" in uploaded_file.content_type or "excel" in uploaded_file.content_type:
            df = pd.read_excel(uploaded_file)
        else:
            return JsonResponse({"error": "Unsupported file format"}, status=400)

        save_dataset(dataset_name, df.to_dict(orient="records"))
        return JsonResponse({"success": True, "dataset_name": dataset_name})
