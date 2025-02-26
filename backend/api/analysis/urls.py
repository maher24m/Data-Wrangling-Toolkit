from django.urls import path
from .views import DataAnalysisView

urlpatterns = [
    path("<str:dataset_name>/", DataAnalysisView.as_view(), name="data-analysis"),
]
