from django.urls import path
from .high_court.hc_scraper import highCourt_API

urlpatterns = [
    path('v1/hc-madras/judgements/case_no', highCourt_API, name="highCourt_API"),
]
