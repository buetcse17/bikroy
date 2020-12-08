from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.list,name='jobs'),
    path('job_id-<slug:job_id>/',views.displayJob,name='DisplayJob'),

    path('<slug:area>/', views.listJobAreaWise, name='listJobAreaWise'),
    path('sendCV/<slug:job_id>/',views.sendCV,name='sendCV')

    
]