from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.mychats, name='mychats'),
    path('chatbox/', views.chatbox, name='chatbox'),
    path('chatbox/<slug:chatUser>/', views.chatbox, name='chatbox'),
]
