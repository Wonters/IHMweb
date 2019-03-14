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

from config.views import Configuration

# rajouter des fichiers url.py dans chaque applications pour éviter une surcharge du dictionnaire urlpatterns du projet
print("url")
config = Configuration()

urlpatterns = [
    path('', config.home, name='home'),
    path('read', config.read, name='read'),
    path('write', config.write, name='write'),
    path('readtc', config.read_testcase, name='readtc'),
    path('create', config.create, name='create'),
    path('delete', config.delete, name='delete'),
    path('addConf', config.add, name='add'),
]
