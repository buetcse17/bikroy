from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.adminDashboard, name='adminDashboard'),
    path('userData/', views.userData, name='userData'),
     # admin
    path('approve/',views.approval, name='approve'),
    path('approveProduct/<slug:update_status>/<int:id>/',views.Productapproval, name='approveProduct'),
    path('approveJob/<slug:update_status>/',views.Jobapproval, name='approveProduct'),
]
