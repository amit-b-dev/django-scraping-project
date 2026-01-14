"""
URL configuration for django_scraping_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('vahan_citizen.urls')),
    path('api/', include('e_court_services.urls')),
    path('api/', include('hc_madras.urls')),
    path('api/', include('karnatakaone.urls')),
    path('api/', include('telangana_challan.urls')),
    path('api/', include('mp_challan.urls')),
    path('api/', include('jharkhand_challan.urls')),
    path('api/', include('gujrat_high_court.urls')),
    path('api/', include('bombay_high_court.urls')),
    path('api/', include('karnataka_high_court.urls')),
    path('api/', include('delhi_high_court.urls')),
    path('api/', include('madras_hc_judgements.urls')),
    path('api/', include('madras_madurai_bench_judgements.urls')),
    path('api/', include('calcutta_hc_all_modules.urls')),
    path('api/', include('ksat_cases.urls')),

]
