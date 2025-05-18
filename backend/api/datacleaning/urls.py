from django.urls import path
from .views import ApplyCleaningView, AvailableCleaningsView

urlpatterns = [
    path('<str:dataset_name>/clean/', ApplyCleaningView.as_view(), name='apply-cleaning'),
    path('', AvailableCleaningsView.as_view(), name='available-cleanings'),
]
