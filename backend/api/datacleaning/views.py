# backend/api/datacleaning/views.py
import json
import pandas as pd
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.datasets.manager import save_dataset, get_dataset # Assuming these exist and work as expected
from api.datacleaning.factory import DataCleaningFactory



@method_decorator(csrf_exempt, name="dispatch")
class ApplyCleaningView(View):
    def post(self, request, dataset_name):
        try:
            # Get the dataset
            df = get_dataset(dataset_name)
            if df is None:
                return JsonResponse(
                    {"error": f"Dataset '{dataset_name}' not found"},
                    status=404
                )
            
            # Parse request body
            try:
                body = json.loads(request.body)
                cleaning_name = body.get('cleaning')
                parameters = body.get('parameters', {})
            except json.JSONDecodeError:
                return JsonResponse(
                    {"error": "Invalid JSON payload"},
                    status=400
                )
            
            if not cleaning_name:
                return JsonResponse(
                    {"error": "Cleaning operation name is required"},
                    status=400
                )
            
            # Get and apply cleaning
            cleaner = DataCleaningFactory.get_cleaner(cleaning_name)
            df = cleaner.clean(df, **parameters)
            
            # Save cleaned dataset
            save_dataset(dataset_name, df)
            
            return JsonResponse({
                "message": "Cleaning operation applied successfully",
                "dataset": dataset_name,
                "rows": len(df),
                "columns": len(df.columns)
            })
            
        except ValueError as e:
            return JsonResponse(
                {"error": str(e)},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {"error": f"Error applying cleaning operation: {str(e)}"},
                status=500
            )

@method_decorator(csrf_exempt, name="dispatch")
class AvailableCleaningsView(View):
    def get(self, request):
        """List all available cleaning operations"""
        try:
            cleanings = DataCleaningFactory.list_cleaners()
            return JsonResponse({"cleanings": cleanings})
        except Exception as e:
            return JsonResponse(
                {"error": f"Error retrieving cleaning operations: {str(e)}"},
                status=500
            )