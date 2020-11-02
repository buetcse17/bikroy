from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),                      # kichu na dile home e thakbe
    path('contact', views.contact, name='contact'),         # /contact dile contact e jabe
    path('about', views.about, name='about'),                # /about dile about e jabe



    # Account related
    path('signup', views.signup, name='signup'),
    path('login', views.handleLogin, name='handleLogin'),
    path('logout', views.handleLogout, name='handleLogout'),
    path('profile', views.profile, name='profile'),


    # Ad related
    path('postAd', views.postAd, name='postAd'),
    path('postProductAd', views.postProductAd, name='postProductAd'),
    path('postJobAd', views.postJobAd, name='postJobAd'),


    # dummy
    path('list', views.list_jobs, name='list_jobs'),

]
