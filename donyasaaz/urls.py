"""donyasaaz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from models.views import *

urlpatterns = [
    path('items/', musicItemHandler),
    path('links/', linkHandler),
    path('test_timezone/', test_timezone),
    path('run_prices/', run_prices),
    path(r'a27a579bdf3c579fb0287ad7eedf13f5.woff', fonta27a579bdf3c579fb0287ad7eedf13f5),
    path(r'font655ba951f59a5b99d8627273e0883638.ttf', font655ba951f59a5b99d8627273e0883638),
    path(r'f9ada7e5233f3a92347b7531c06f2336.woff2', fontf9ada7e5233f3a92347b7531c06f2336),
    path(r'',include('models.urls')),
]
