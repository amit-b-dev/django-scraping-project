from django.urls import path
from .high_court.highCourt_Scrape import highCourt_API,caseTypeList_API

urlpatterns = [
    path('v1/hc-delhi/cases/case-no', highCourt_API, name="highCourt_API"),
    path('v1/hc-delhi/case-type-list/', caseTypeList_API, name="caseTypeList_API"),
]
