from django.urls import path
from .high_court.highCourt_Scrape import highCourt_API

urlpatterns = [
    path('v1/hc-delhi/cases/case-no', highCourt_API, name="highCourt_API"),
]
