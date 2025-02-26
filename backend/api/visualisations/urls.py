from django.urls import path
from .views import VisualizationView

urlpatterns = [
    path("<str:dataset_name>/<str:chart_type>/", VisualizationView.as_view(), name="visualization"),
]
