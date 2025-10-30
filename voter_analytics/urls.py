# voter_analytics/urls.py
from django.urls import path
from .views import VotersListView, VoterRecordView

app_name = "voter_analytics"

urlpatterns = [
    path('', VotersListView.as_view(), name='voters'),
    path('voter/<int:pk>', VoterRecordView.as_view(), name='voter')
]


