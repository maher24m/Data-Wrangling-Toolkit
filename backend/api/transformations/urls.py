from django.urls import path
from .views import ApplyTransformationView, AvailableTransformationsView

urlpatterns = [
    path('<str:dataset_name>/transform/', ApplyTransformationView.as_view(), name='apply-transformation'),
    path('', AvailableTransformationsView.as_view(), name='available-transformations'),
]
