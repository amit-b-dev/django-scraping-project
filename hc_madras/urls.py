from django.urls import path
from .views import e_court_services_cnr_no

urlpatterns = [
    path('v1/hc-madras/cnr', e_court_services_cnr_no, name="e_court_services_cnr_no"),
]
