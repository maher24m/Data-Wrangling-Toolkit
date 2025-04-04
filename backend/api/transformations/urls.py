from django.urls import path
from .views import ApplyTransformationView, AvailableTransformationToolsView

urlpatterns = [
    path("", ApplyTransformationView.as_view(), name="apply-transformation"),
    path("tools/", AvailableTransformationToolsView.as_view(), name="available-transformation-tools"),
]
