from django.urls import path
from .vahan.vahan_scraper import vahan_timeline,vahan_transactions_list,vahan_timeline_via_s_no,form29

urlpatterns = [
    path('v1/vahan/timeline', vahan_timeline, name="vahan_timeline"),
    path('v1/vahan/timeline/by-serial', vahan_timeline_via_s_no, name="vahan_timeline_via_s_no"),
    path('v1/vahan/transactions', vahan_transactions_list, name="vahan_transactions_list"),
    path('v1/vahan/form29', form29, name="form29"),
]
