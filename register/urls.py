from django.shortcuts import redirect
from django.urls import path, include
import main.views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),

]
