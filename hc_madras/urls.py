from django.urls import path
from .high_court.hc_scraper import hc_madras_data_by_cnr_no

urlpatterns = [
    path('v1/hc-madras/cnr', hc_madras_data_by_cnr_no, name="hc_madras_data_by_cnr_no"),
]
