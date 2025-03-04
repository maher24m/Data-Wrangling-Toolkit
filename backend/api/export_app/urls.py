from django.urls import path
from .views import DatasetExportView

urlpatterns = [
    path("<str:dataset_name>/<str:file_type>/", DatasetExportView.as_view(), name="dataset-export"),
]
