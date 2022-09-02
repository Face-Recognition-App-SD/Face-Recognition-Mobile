"""Facial_Recognition_Mobile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.urls import include, re_path
# from django.urls import url, include
from Facial_Recognition_App import views


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.index, name = 'index'),
    re_path(r'^Facial_Recognition_App/', include('Facial_Recognition_App.urls')),
    re_path(r'^logout/$', views.user_logout, name = 'logout'),
    re_path(r'^special/',views.special, name = 'special'),
]
