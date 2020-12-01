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
    path('logout/', views.handleLogout, name='handleLogout'),
    path('profile/', views.profile, name='profile'),


    # Ad related
    path('postAd/', views.postAd, name='postAd'),
    path('postProductAd/', views.postProductAd, name='postProductAd'),
    path('productAdCategory/', views.productAdCategory, name='productAdCategory'),
    path('productAdCategory/<int:id>/', views.productAdCategory, name='productAdCategory'),
    path('postJobAd/', views.postJobAd, name='postJobAd'),

    # admin
    path('approve/',views.approval, name='approve'),
    path('admin/approveProduct/<slug:update_status>/<int:id>/',views.Productapproval, name='approveProduct'),
    path('admin/approveJob/<slug:update_status>/',views.Jobapproval, name='approveProduct'),
    #profile
    path('profile/addEdu/', views.addEdu, name='addEdu'),
    path('profile/addWork/', views.addWork, name='addWork'),
    path('profile/deleteEdu/<slug:institution_id>/', views.deleteEdu, name='deleteEdu'),
    path('profile/changeEdu/<slug:institution_id>/', views.editEdu, name='editEdu'),
    path('profile/deleteWork/<slug:organization_id>/', views.deleteWork, name='deleteWork'),
    path('profile/changeWork/<slug:organization_id>/', views.editWork, name='editWork'),
    path('myAds/', views.myAds, name='myAds'),

    #Myads
    path('deleteAd/<slug:product_id>/', views.deleteAd, name='deleteAd'),

    # dummy
    path('list', views.list_jobs, name='list_jobs'),

]
