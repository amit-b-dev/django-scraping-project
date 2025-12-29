from django.urls import path
from .eCourtServices.eCourt_Scrape import eCourtServices_API

urlpatterns = [
    path('v1/ecourt/cnr', eCourtServices_API, name="eCourtServices_API"),
]

# from django.urls import path
# from .views import e_court_services_cnr_no

# urlpatterns = [
#     path('v1/ecourt/cnr', e_court_services_cnr_no, name="e_court_services_cnr_no"),
# ]

