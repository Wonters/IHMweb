#!/usr/bin/python3 
# coding=UTF-8
"""test_bench URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path

from testcase.views import Caracterisation

carac = Caracterisation()  # obligation d'initialiser pour lire le constructeur

# url of testcase application

urlpatterns = [
    path('', carac.home, name='home'),
    path('start', carac.start, name='start'),
    path('stop', carac.stop, name='stop'),
    path('load', carac.load, name='load'),
    path('readtc', carac.readtc, name='readtc'),
    path('counter', carac.counter, name='counter'),
    path('writeschedule', carac.write_schedule, name='write schedule'),
]
