# backend/api/datacleaning/views.py
import json
import pandas as pd
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from api.datasets.manager import save_dataset, get_active_dataset, get_active_dataset_name, get_dataset
from api.datacleaning.factory import DataCleaningFactory


@method_decorator(csrf_exempt, name="dispatch")
class DataCleaningView(View):
    """
    Accepts a JSON body of the form:
      { "operations": [ { "type": "...", ... }, { "type": "...", ... }, … ] }
    Applies each in turn to the single 'active' dataset and re-saves it.
    """

    def post(self, request):
        # 1) parse JSON body
        try:
            body = json.loads(request.body)
            ops = body.get("operations")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        if not isinstance(ops, list):
            return JsonResponse({"error": "`operations` must be a list"}, status=400)

        # 2) load the one-and-only active dataset
        raw = get_dataset("pepe")
        if raw is None:
            return JsonResponse({"error": f"Dataset not found."}, status=404)

        df = pd.DataFrame(raw)

        # 3) apply each operation in sequence
        for op in ops:
            op_type = op.get("type")
            if not op_type:
                return JsonResponse({"error": "Each operation must include a 'type'"}, status=400)

            try:
                processor = DataCleaningFactory.get_processor(op_type)
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)

            # build kwargs for .apply() from everything except "type"
            params = {k: v for k, v in op.items() if k != "type"}
            try:
                df = processor.apply(df, **params)
            except Exception as e:
                return JsonResponse({
                    "error": f"Failed to apply '{op_type}'",
                    "details": str(e)
                }, status=500)

        # 4) save back
        save_dataset(get_active_dataset_name(), df.to_dict(orient="records"))

        return JsonResponse({
            "success": True,
            "message": f"Applied {len(ops)} operations successfully"
        })


@method_decorator(csrf_exempt, name="dispatch")
class AvailableCleaningToolsView(View):
    """Lists all available cleaning operations."""
    def get(self, request):
        return JsonResponse({
            "cleaning_tools": DataCleaningFactory.list_processors()
        })
