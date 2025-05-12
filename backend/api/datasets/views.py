from django.views import View
from django.http import JsonResponse
from api.datasets.manager import get_dataset, list_datasets, delete_dataset, save_dataset
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

class DatasetListView(View):
    """Returns a list of available datasets"""
    def get(self, request):
        return JsonResponse({"datasets": list_datasets()})

@method_decorator(csrf_exempt, name="dispatch")
class DatasetDetailView(View):
    """Fetches a dataset by name and ensures response is proper JSON"""
    def get(self, request, dataset_name, chunk_size=None):
        dataset = get_dataset(dataset_name, chunk_size)
        if dataset is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        try:
            # Convert to records format first
            records = json.loads(dataset.to_json(orient="records"))
            # Transform each value into {value: actual_value} format
            formatted_data = []
            for record in records:
                row = []
                for val in record.values():
                    row.append({"value": val})
                formatted_data.append(row)
            return JsonResponse({"values": formatted_data})
        except Exception as e:
            return JsonResponse({"error": "JSON serialization failed", "details": str(e)}, status=500)

@method_decorator(csrf_exempt, name="dispatch")
class DatasetDeleteView(View):
    """Deletes a dataset by name.
    
    If the dataset does not exist, the function will still return a success message,
    as it assumes the dataset is already deleted or never existed."""
    def delete(self, request, dataset_name):
        try:
            delete_dataset(dataset_name)
            return JsonResponse({"message": f"Dataset '{dataset_name}' deleted successfully."})
        except Exception as e:
            return JsonResponse({"error": "Failed to delete dataset", "details": str(e)}, status=500)

@method_decorator(csrf_exempt, name="dispatch")
class DatasetSaveView(View):
    """Handles saving updates to a dataset.
    
    Expects a POST request with JSON data containing the updated dataset.
    The data should be in the format:
    {
        "data": [
            {"column1": "value1", "column2": "value2", ...},
            ...
        ]
    }
    """
    def post(self, request, dataset_name):
        try:
            # Parse the request body
            body = json.loads(request.body)
            
            if 'data' not in body:
                return JsonResponse({
                    "error": "Missing 'data' field in request body"
                }, status=400)

            # Get the current dataset to verify it exists
            current_dataset = get_dataset(dataset_name)
            if current_dataset is None:
                return JsonResponse({
                    "error": f"Dataset '{dataset_name}' not found"
                }, status=404)

            # Save the updated data
            save_dataset(dataset_name, body['data'])

            # Return success response with the updated data
            return JsonResponse({
                "message": f"Dataset '{dataset_name}' updated successfully",
                "data": body['data']
            })

        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON in request body"
            }, status=400)
        except Exception as e:
            return JsonResponse({
                "error": "Failed to save dataset",
                "details": str(e)
            }, status=500)