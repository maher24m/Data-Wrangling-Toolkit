from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.storage import save_dataset
from api.import_app.factory import FileProcessorFactory


@method_decorator(csrf_exempt, name="dispatch")  # 🔥 Disable CSRF for this view
class FileUploadView(View):
    """Uploads a dataset file and stores it."""
    
    def post(self, request):
        if "file" not in request.FILES or "dataset_name" not in request.POST:
            return JsonResponse({"error": "File and dataset name required"}, status=400)

        dataset_name = request.POST["dataset_name"]
        uploaded_file = request.FILES["file"]
        file_type = uploaded_file.content_type  # Detect file type
        print(file_type)
        try:
            processor = FileProcessorFactory.get_processor(file_type)
            df = processor.process(uploaded_file)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Failed to process file", "details": str(e)}, status=500)

        # Store dataset
        save_dataset(dataset_name, df.to_dict(orient="records"))
        return JsonResponse({"success": True, "dataset_name": dataset_name, "columns": df.columns.tolist()})

@method_decorator(csrf_exempt, name="dispatch")
class AvailableImportToolsView(View):
    """Returns a list of available file import processors from the factory"""
    def get(self, request):
        return JsonResponse({
            "import_tools": FileProcessorFactory.list_processors()
        })