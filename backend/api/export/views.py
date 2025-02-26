from django.views import View
from django.http import HttpResponse, JsonResponse
import pandas as pd
from api.storage import get_dataset

class DatasetExportView(View):
    """Exports dataset as CSV or Excel."""
    def get(self, request, dataset_name, file_type):
        dataset = get_dataset(dataset_name)
        if dataset is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        df = pd.DataFrame(dataset)

        if file_type == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = f'attachment; filename="{dataset_name}.csv"'
            df.to_csv(path_or_buf=response, index=False)
        elif file_type == "excel":
            response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = f'attachment; filename="{dataset_name}.xlsx"'
            df.to_excel(response, index=False)
        else:
            return JsonResponse({"error": "Unsupported export format"}, status=400)

        return response
