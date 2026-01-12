from django.urls import path
from .high_court.highCourt_Scrape import highCourt_API, caseTypeList_API, benchTypeList_API

urlpatterns = [
    path('k1/hc-karnataka/cases/case-no', highCourt_API, name="highCourt_API"),
    path('k1/hc-karnataka/bench-type-list', benchTypeList_API, name="benchTypeList_API"),
    path('k1/hc-karnataka/case-type-list', caseTypeList_API, name="caseTypeList_API"),

]
