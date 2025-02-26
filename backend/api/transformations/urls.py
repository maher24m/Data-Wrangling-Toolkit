from django.urls import path
from .views import ApplyTransformationView

urlpatterns = [
    path("<str:dataset_name>/", ApplyTransformationView.as_view(), name="apply-transformation"),
]
