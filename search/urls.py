from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.searchHome, name='searchHome'),
    path('<slug:query>/', views.searchItem, name='searchItem'),
    path('<slug:query>/<slug:area>/', views.searchAreaWise, name='searchAreaWise')
]
