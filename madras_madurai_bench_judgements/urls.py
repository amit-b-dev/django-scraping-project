from django.urls import path
from .high_court.hc_scraper import hcMadrasMaduraiBench_API, caseTypeList_API

urlpatterns = [
    path('m2/hc-madras/madurai-bench/judgements/case_no', hcMadrasMaduraiBench_API, name="highCourt_API"),
    path('m2/hc-madras/madurai-bench/judgements/case-type-list', caseTypeList_API, name="caseTypeList_API"),

]
