from django.views import View
from django.http import JsonResponse
from api.datasets.manager import get_dataset, save_dataset
from api.transformations.factory import TransformationProcessorFactory
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

@method_decorator(csrf_exempt, name="dispatch")
class ApplyTransformationView(View):
    """Applies transformations to the active dataset"""
    
    def post(self, request):
        dataset_name = request.POST.get("dataset_name")
        transformations = request.POST.getlist("transformations")  # Expecting a JSON list
 
        if not dataset_name or not transformations:
            return JsonResponse({"error": "Missing required parameters"}, status=400)

        try:
            transformations = json.loads(transformations[0])  # Parse JSON array
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format for transformations"}, status=400)

        df = get_dataset(dataset_name)
        if df is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        try:
            for transformation in transformations:
                transformation_type = transformation.get("type")
                column_name = transformation.get("column")

                if column_name not in df.columns:
                    return JsonResponse({"error": f"Column '{column_name}' not found"}, status=400)

                processor = TransformationProcessorFactory.get_processor(transformation_type)
                df = processor.apply(df, column_name)

            transformed_name = f"{dataset_name}_transformed"
            save_dataset(transformed_name, df.to_dict(orient="records"))
            return JsonResponse({"success": True, "dataset": transformed_name})

        except Exception as e:
            return JsonResponse({"error": "Transformation failed", "details": str(e)}, status=500)

@method_decorator(csrf_exempt, name="dispatch")
class AvailableTransformationToolsView(View):
    """Returns a list of available transformations from the factory"""
    def get(self, request):
        return JsonResponse({
            "transformation_tools": TransformationProcessorFactory.list_processors()  # 🔥 Uses lazy-loaded factory
        })