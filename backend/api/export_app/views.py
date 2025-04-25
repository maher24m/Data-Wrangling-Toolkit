# api/export_app/views.py

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.storage import get_dataset
from api.export_app.factory import FileExporterFactory
import os

@method_decorator(csrf_exempt, name="dispatch")
class FileExportView(View):
    """Exports a dataset to a file."""

    def post(self, request):
        if "dataset_name" not in request.POST or "file_type" not in request.POST:
            return JsonResponse({"error": "Dataset name and file type required"}, status=400)

        dataset_name = request.POST["dataset_name"]
        file_type = request.POST["file_type"]
        
        # Use provided file_path or generate a default one in the downloads directory
        file_path = request.POST.get("file_path")
        if not file_path:
            downloads_dir = "exports"
            # Create downloads directory if it doesn't exist
            os.makedirs(downloads_dir, exist_ok=True)
            file_path = os.path.join(downloads_dir, f"{dataset_name}.{file_type}")

        try:
            data = get_dataset(dataset_name)
        except Exception as e:
            return JsonResponse({"error": "Failed to load dataset", "details": str(e)}, status=500)

        if data is None:
            return JsonResponse({"error": f"Dataset '{dataset_name}' not found."}, status=404)

        try:
            exporter = FileExporterFactory.get_exporter(file_type)
            exporter.export(data, file_path)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Failed to export file", "details": str(e)}, status=500)

        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type=file_type)
            response["Content-Disposition"] = f"attachment; filename={os.path.basename(file_path)}"
            return response
        

@method_decorator(csrf_exempt, name="dispatch")
class AvailableExportToolsView(View):
    """Returns a list of available file export tools from the factory."""
    def get(self, request):
        return JsonResponse({
            "export_tools": FileExporterFactory.list_exporters()
        })