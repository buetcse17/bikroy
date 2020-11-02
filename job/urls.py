from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.list,name='jobs'),
    path('<slug:job_id>/',views.displayJob,name='DisplayJob')
    
]