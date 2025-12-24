from django.urls import path
from .telanganaChallan.telangana_Scrape import telanganaChallan_API

urlpatterns = [
    path('v1/telangana/challan/vehicle_no', telanganaChallan_API, name="telanganaChallan_API"),
]
