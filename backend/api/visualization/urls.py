from django.urls import path
from .views import ApplyVisualizationView, AvailableVisualizationsView

app_name = 'visualization'

urlpatterns = [
    path('<str:dataset_name>/visualize/', ApplyVisualizationView.as_view(), name='apply-visualization'),
    path('', AvailableVisualizationsView.as_view(), name='available-visualizations'),
] 