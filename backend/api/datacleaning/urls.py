from django.urls import path
from .views import DataCleaningView, AvailableCleaningToolsView

urlpatterns = [
    path("<str:dataset_name>/", DataCleaningView.as_view(), name="data-cleaning"),
    path("tools/", AvailableCleaningToolsView.as_view(), name="available-cleaning-tools"),
]
