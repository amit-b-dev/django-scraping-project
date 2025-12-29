from django.urls import path
from .mpChallan.mp_Scrape import mpChallan_API

urlpatterns = [
    path('v1/mp/challan/vehicle_no', mpChallan_API, name="mpChallan_API"),
]
