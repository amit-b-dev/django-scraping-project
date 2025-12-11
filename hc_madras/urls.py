from django.urls import path
from .views import hc_madras_data_by_cnr_no

urlpatterns = [
    path('v1/hc-madras/cnr', hc_madras_data_by_cnr_no, name="hc_madras_data_by_cnr_no"),
]
