from django.urls import path
from .high_court.highCourt_Scrape import hc_madras_data_by_cnr_no

urlpatterns = [
    path('v1/hc-madras/cases/cnr_no', hc_madras_data_by_cnr_no, name="hc_madras_data_by_cnr_no"),
]
