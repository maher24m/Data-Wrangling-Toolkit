# api/datasets/urls.py
from django.urls import path
from .views import DatasetListView, DatasetDetailView, DatasetDeleteView, DatasetSaveView

app_name = "datasets"    # ← this must match the namespace you’ll use below

urlpatterns = [
    path(
        "",
        DatasetListView.as_view(),
        name="dataset-list"
    ),  # List all datasets
    path(
        "<str:dataset_name>/",
        DatasetDetailView.as_view(),
        name="dataset-detail"
    ),  # Fetch a specific dataset
    path(
        "<str:dataset_name>/delete/",
        DatasetDeleteView.as_view(),
        name="dataset-delete"
    ), # Delete a specific dataset
    path(
        "<str:dataset_name>/save/",
        DatasetSaveView.as_view(),
        name="dataset-save"
    ), # Save a specific dataset

]
