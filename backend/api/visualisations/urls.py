from django.urls import path
from .views import VisualizationView, AvailableVisualizationsView

urlpatterns = [
    path("<str:dataset_name>/<str:chart_type>/", VisualizationView.as_view(), name="visualization"),
    path("types/", AvailableVisualizationsView.as_view(), name="available_visualizations"),
]
