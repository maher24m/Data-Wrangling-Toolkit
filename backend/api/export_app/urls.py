# api/export_app/urls.py
from django.urls import path
from .views import FileExportView, AvailableExportToolsView

app_name = "export_app"

urlpatterns = [
    path("", FileExportView.as_view(), name="file_export"),
    path("tools/", AvailableExportToolsView.as_view(), name="available_export_tools"),
]
