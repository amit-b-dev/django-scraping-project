from django.urls import path
from .ka_chalan.ka_chalan_scraper import send_otp_api, validate_api

urlpatterns = [
    # path('k1/karnataka/chalan/regno', karnatakaOneChalanByRegNo, name="karnatakaOneChalanByRegNo"),
    path('k1/karnataka/chalan/sendOTP', send_otp_api, name="send_otp_api"),
    path('k1/karnataka/chalan/validateOTP', validate_api, name="validate_api"),
]
