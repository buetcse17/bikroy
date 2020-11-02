from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [                     # kichu na dile home e thakbe
    path('', views.products, name='product'),
    path('<int:id>/',views.list, name='listProduct'),
    path('<int:id>/<slug:product_id>/',views.displayProduct, name='DisplayProduct')
               # /about dile about e jabe
 ]
