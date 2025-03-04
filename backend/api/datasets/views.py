from django.views import View
from django.http import JsonResponse
from api.storage import get_dataset

class DatasetDetailView(View):
    """Fetches a dataset but limits the number of rows returned for performance."""

    def get(self, request, dataset_name):
        dataset = get_dataset(dataset_name)
        if dataset is None:
            return JsonResponse({"error": "Dataset not found"}, status=404)

        max_rows = int(request.GET.get("limit", 1000))  # Limit rows (default: 1000)
        df = dataset.head(max_rows)  # Load only required rows

        return JsonResponse({"data": df.to_dict(orient="records")})
