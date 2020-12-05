from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.adminDashboard, name='adminDashboard'),
    path('userData/', views.userData, name='userData'),
]
