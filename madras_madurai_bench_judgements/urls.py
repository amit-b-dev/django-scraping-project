from django.urls import path
from .high_court.hc_scraper import hcMadrasMaduraiBench_API

urlpatterns = [
    path('v1/hc-madras/madurai-bench/judgements/case_no', hcMadrasMaduraiBench_API, name="highCourt_API"),
]
