# backend/api/datacleaning/views.py
import json
import pandas as pd
from django.views import View
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# --- FIX: Use functions consistent with tests/assumptions ---
from api.datasets.manager import save_dataset # Assuming these exist and work as expected
from api.datacleaning.factory import DataCleaningFactory
import traceback # For more detailed error logging


@method_decorator(csrf_exempt, name="dispatch")
class DataCleaningView(View):
    """
    Accepts a JSON body of the form:
      { "operations": [ { "type": "...", ...params }, { "type": "...", ...params }, … ] }
    Applies each operation in turn to the 'active' dataset and saves it back.
    """

    def post(self, request):
        # 1) Parse JSON body
        try:
            body = json.loads(request.body)
            ops = body.get("operations")
            if not isinstance(ops, list):
                return JsonResponse({"error": "`operations` must be a list"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)
        except Exception as e: # Catch broader errors during parsing
             return JsonResponse({"error": f"Error processing request body: {e}"}, status=400)


        # 2) Load the active dataset
        try:
            # --- FIX: Use get_active_dataset ---
            df = get_dataset("active_dataset") # Assuming this function exists and works as expected
            if df is None:
                # --- FIX: Return 404 if no active dataset ---
                return JsonResponse({"error": "Active dataset not found or is empty."}, status=404)
            if not isinstance(df, pd.DataFrame):
                 try:
                     df = pd.DataFrame(df)
                 except Exception as e:
                      print(f"Error converting loaded data to DataFrame: {e}")
                      return JsonResponse({"error": "Failed to load dataset as DataFrame"}, status=500)

        except FileNotFoundError: # Specific exception if manager raises it
             return JsonResponse({"error": "Active dataset file not found."}, status=404)
        except Exception as e:
            print(f"Error loading active dataset: {e}")
            return JsonResponse({"error": "Failed to load active dataset"}, status=500)


        # 3) Apply each operation in sequence
        original_df = df # Keep original for potential rollback or comparison if needed

        for i, op in enumerate(ops):
            if not isinstance(op, dict):
                 return JsonResponse({"error": f"Operation at index {i} is not a valid JSON object."}, status=400)

            op_type = op.get("type")
            if not op_type:
                return JsonResponse({"error": f"Operation at index {i} must include a 'type' key."}, status=400)

            try:
                processor = DataCleaningFactory.get_processor(op_type)
            except ValueError as e: # Raised by get_processor if type not found
                return JsonResponse({"error": str(e)}, status=400)
            except Exception as e: # Catch other factory errors
                 print(f"Error getting processor for type '{op_type}': {e}")
                 return JsonResponse({"error": f"Internal error retrieving processor for '{op_type}'"}, status=500)


            # Build kwargs for .apply() from everything except "type"
            params = {k: v for k, v in op.items() if k != "type"}
            try:
                df = processor.apply(df, **params)
                if not isinstance(df, pd.DataFrame):
                     print(f"Error: Processor '{op_type}' did not return a pandas DataFrame.")
                     return JsonResponse({"error": f"Operation '{op_type}' failed internally (invalid return type)."}, status=500)

            except ValueError as e: # Catch parameter errors from apply methods
                 return JsonResponse({
                     "error": f"Invalid parameters for operation '{op_type}' at index {i}",
                     "details": str(e)
                 }, status=400)
            except Exception as e:
                # Log the full traceback for debugging
                print(f"Error applying operation '{op_type}' (index {i}):\n{traceback.format_exc()}")
                return JsonResponse({
                    "error": f"Failed to apply operation '{op_type}' at index {i}",
                    "details": str(e) # Return a user-friendly error message
                }, status=500)

        # 4) Save back the modified dataset
        try:
            # --- FIX: Use get_active_dataset_name ---
            active_dataset_name = getdataset_name()
            if not active_dataset_name:
                 # This case might indicate an issue with the manager setup
                 print("Error: Could not determine active dataset name for saving.")
                 return JsonResponse({"error": "Failed to save dataset: Cannot determine active dataset name."}, status=500)

            # Convert DataFrame back to the format expected by save_dataset (e.g., list of dicts)
            # Adjust 'orient' based on what save_dataset expects. 'records' is common.
            data_to_save = df.to_dict(orient="records")
            save_dataset(active_dataset_name, data_to_save)

        except Exception as e:
             print(f"Error saving processed dataset '{active_dataset_name}':\n{traceback.format_exc()}")
             # Optionally try to restore the original? Depends on requirements.
             return JsonResponse({"error": "Failed to save the processed dataset."}, status=500)

        return JsonResponse({
            "success": True,
            "message": f"Applied {len(ops)} operations successfully to dataset '{active_dataset_name}'.",
            # Optional: return number of rows/cols?
            "rows": len(df),
            "columns": len(df.columns)
        })


@method_decorator(csrf_exempt, name="dispatch")
class AvailableCleaningToolsView(View):
    """Lists all available cleaning operation types."""
    def get(self, request):
        try:
            tools = DataCleaningFactory.list_processors()
            return JsonResponse({
                "cleaning_tools": tools
            })
        except Exception as e:
             print(f"Error listing cleaning tools: {e}")
             return JsonResponse({"error": "Failed to retrieve available cleaning tools."}, status=500)