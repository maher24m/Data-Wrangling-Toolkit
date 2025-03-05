from django.urls import path, include

urlpatterns = [
    path("datasets/", include("api.datasets.urls")),  # Dataset Management
    path("import/", include("api.import_app.urls")),  # File Import API
    path("export/", include("api.export_app.urls")),  # File Export API
    path("transformations/", include("api.transformations.urls")),  # Data Transformations
    path("visualisations/", include("api.visualisations.urls")),  # Data Visualization API
    path("analysis/", include("api.analysis.urls")),  # Data Analysis API
    path("datacleaning/", include("api.datacleaning.urls")),  # Data Cleaning API
]
