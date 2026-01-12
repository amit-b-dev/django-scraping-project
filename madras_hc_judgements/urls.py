from django.urls import path
from .high_court.hc_scraper import highCourt_API,caseTypeList_API

urlpatterns = [
    path('m1/hc-madras/judgements/case_no', highCourt_API, name="highCourt_API"),
    path('m1/hc-madras/judgements/case-type-list', caseTypeList_API, name="caseTypeList_API"),

]
