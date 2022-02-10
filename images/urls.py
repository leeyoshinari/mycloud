#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
from django.urls import path
from . import views

app_name = 'images'
urlpatterns = [
    path('login', views.login, name='login'),
    path('', views.home, name='home'),
    path('folder/create', views.create_folder, name='create_folder'),
    path('folder/delete', views.delete_folder, name='delete_folder')
]
