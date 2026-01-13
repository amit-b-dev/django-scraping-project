from django.urls import path
from .high_court.highCourt_Scrape import highCourt_API,caseTypeList_API, caseModeList_API

urlpatterns = [
    path('g1/hc-gujrat/cases/case-no', highCourt_API, name="highCourt_API"),
    path('g1/hc-gujrat/case-mode-list', caseModeList_API, name="caseModeList_API"),
    path('g1/hc-gujrat/case-type-list', caseTypeList_API, name="caseTypeList_API"),
]
