# project/urls.py
from django.urls import path, include

urlpatterns = [
    path(
        "datasets/",
        include(("api.datasets.urls", "datasets"), namespace="datasets")
    ),  # Dataset Management
    path(
        "import/",
        include(("api.import_app.urls", "import_app"), namespace="import_app")
    ),  # File Import API
    path(
        "export/",
        include(("api.export_app.urls", "export_app"), namespace="export_app")
    ),  # File Export API
    path(
        "transformations/",
        include(("api.transformations.urls", "transformations"), namespace="transformations")
    ),  # Data Transformations
    path(
        "visualisations/",
        include(("api.visualisations.urls", "visualisations"), namespace="visualisations")
    ),  # Data Visualization API
    path(
        "analysis/",
        include(("api.analysis.urls", "analysis"), namespace="analysis")
    ),  # Data Analysis API
    path(
        "datacleaning/",
        include(("api.datacleaning.urls", "datacleaning"), namespace="datacleaning")
    ),  # Data Cleaning API
]
