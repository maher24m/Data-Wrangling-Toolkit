from django.views import View
from django.http import HttpResponse, JsonResponse
import pandas as pd
from api.storage import get_dataset
from api.export_app.export_processors import ExportProcessorFactory  # New

class DatasetExportView(View):
    """Exports dataset as CSV, Excel, or other supported formats."""

    def get(self, request, dataset_name, file_type):
        dataset = get_dataset(dataset_name)
        if dataset is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        df = pd.DataFrame(dataset)

        try:
            processor = ExportProcessorFactory.get_processor(file_type)
            response = processor.export(df, dataset_name)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Export failed", "details": str(e)}, status=500)

        return response
