from django.urls import path
from .jharkhandChallan.jharkhand_Scrape import jharkhandChallan_API
urlpatterns = [
    path('v1/jharkhand/challan/vehicle_no', jharkhandChallan_API, name="jharkhandChallan_API"),
]
