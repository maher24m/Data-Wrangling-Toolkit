# api/urls.py

from django.urls import path
from api.export_app.views import FileExportView, AvailableExportToolsView

urlpatterns = [
    path("", FileExportView.as_view(), name="file_export"),
    path("tools", AvailableExportToolsView.as_view(), name="available_export_tools"),
]