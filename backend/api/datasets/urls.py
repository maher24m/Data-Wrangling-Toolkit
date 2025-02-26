from django.urls import path
from .views import DatasetListView, DatasetDetailView

urlpatterns = [
    path("", DatasetListView.as_view(), name="dataset-list"),
    path("<str:dataset_name>/", DatasetDetailView.as_view(), name="dataset-detail"),
]
