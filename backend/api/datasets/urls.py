from django.urls import path
from .views import DatasetDetailView

urlpatterns = [
    path("<str:dataset_name>/", DatasetDetailView.as_view(), name="dataset-detail"),
]
