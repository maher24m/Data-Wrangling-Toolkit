from django.urls import path
from .views import DataCleaningView

urlpatterns = [
    path("<str:dataset_name>/", DataCleaningView.as_view(), name="data-cleaning"),
]
