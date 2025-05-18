from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .factory import AnalysisFactory
from ..datasets.manager import get_dataset

@method_decorator(csrf_exempt, name="dispatch")
class ApplyAnalysisView(View):
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
                analysis_name = body.get('analysis')
                parameters = body.get('parameters', {})
            except json.JSONDecodeError:
                return JsonResponse(
                    {"error": "Invalid JSON payload"},
                    status=400
                )
            
            if not analysis_name:
                return JsonResponse(
                    {"error": "Analysis name is required"},
                    status=400
                )
            
            # Get and apply analysis
            analysis = AnalysisFactory.get_analysis(analysis_name)
            results = analysis.analyze(df, **parameters)
            
            return JsonResponse({
                "message": "Analysis completed successfully",
                "dataset": dataset_name,
                "analysis": analysis_name,
                "results": results
            })
            
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": "Failed to perform analysis", "details": str(e)},
                status=500
            )

@method_decorator(csrf_exempt, name="dispatch")
class AvailableAnalysesView(View):
    def get(self, request):
        """Returns a list of available analyses"""
        try:
            analyses = AnalysisFactory.list_analyses()
            return JsonResponse({
                "analyses": analyses
            })
        except Exception as e:
            return JsonResponse(
                {"error": "Failed to list analyses", "details": str(e)},
                status=500
            )
