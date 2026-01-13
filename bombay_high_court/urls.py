from django.urls import path
from .high_court.highCourt_Scrape import highCourt_API, caseSideList_API, caseTypeList_API, stampAndRegList_API

urlpatterns = [
    path('b1/hc-bombay/cases/case-no', highCourt_API, name="highCourt_API"),
    path('b1/hc-bombay/case-side-list', caseSideList_API, name="caseSideList_API"),
    path('b1/hc-bombay/case-stam-reg-list', stampAndRegList_API, name="stampAndRegList_API"),
    path('b1/hc-bombay/case-type-list', caseTypeList_API, name="caseTypeList_API"),
]
