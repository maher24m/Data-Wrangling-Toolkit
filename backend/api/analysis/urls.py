from django.urls import path
from .views import ApplyAnalysisView, AvailableAnalysesView

app_name = 'analysis'

urlpatterns = [
    path('<str:dataset_name>/analyze/', ApplyAnalysisView.as_view(), name='apply-analysis'),
    path('', AvailableAnalysesView.as_view(), name='available-analyses'),
]
