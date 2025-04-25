from django.views import View
from django.http import JsonResponse
import pandas as pd
import json
from api.storage import get_dataset, save_dataset
from api.datacleaning.factory import CleaningProcessorFactory
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name="dispatch")
class DataCleaningView(View):
    """Handles dataset cleaning operations"""
    def post(self, request, dataset_name):
        dataset = get_dataset(dataset_name)
        if dataset is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        try:
            # Parse the cleaning operations from the request
            operations_data = request.POST.get("operations")
            if not operations_data:
                return JsonResponse({"error": "No cleaning operations provided"}, status=400)
            
            operations = json.loads(operations_data)
            if not isinstance(operations, list):
                operations = [operations]  # Handle single operation case
            
            df = pd.DataFrame(dataset)
            
            # Apply each cleaning operation
            for operation in operations:
                operation_type = operation.get("type")
                if not operation_type:
                    return JsonResponse({"error": "Missing operation type"}, status=400)
                
                # Get the processor for this operation type
                processor = CleaningProcessorFactory.get_processor(operation_type)
                
                # Apply the processor with any additional parameters
                params = {k: v for k, v in operation.items() if k != "type"}
                df = processor.apply(df, **params)
            
            # Save the cleaned dataset
            save_dataset(dataset_name, df.to_dict(orient="records"))
            return JsonResponse({"success": True, "message": "Cleaning operations applied successfully"})
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format for operations"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Cleaning operation failed", "details": str(e)}, status=500)

@method_decorator(csrf_exempt, name="dispatch")
class AvailableCleaningToolsView(View):
    """Returns a list of available cleaning operations from the factory"""
    def get(self, request):
        return JsonResponse({
            "cleaning_tools": CleaningProcessorFactory.list_processors()
        })
