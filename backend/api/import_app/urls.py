from django.urls import path
from .views import FileUploadView, AvailableImportToolsView

urlpatterns = [
    path("", FileUploadView.as_view(), name="file-upload"),
    path("tools/", AvailableImportToolsView.as_view(), name="available-import-tools"),
]
