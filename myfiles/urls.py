#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
from django.urls import path
from . import views

app_name = 'myfiles'
urlpatterns = [
    path('login', views.login, name='login'),
    path('', views.home, name='home'),
    path('folder/create', views.create_folder, name='create_folder'),
    path('folder/rename', views.rename_folder, name='rename_folder'),
    path('folder/delete', views.delete_folder, name='delete_folder'),
    path('folder/return', views.return_last_path, name='return_folder'),
    path('file/search', views.search_file, name='search_file'),
    path('file/rename', views.rename_file, name='rename_file'),
    path('file/delete', views.delete_file, name='delete_file'),
    path('findOriginPath', views.find_origin_path, name='find_origin_path'),
    path('getFiles', views.get_all_files, name='get_all_files'),
    path('getRecentFiles', views.get_recent_files, name='get_recent_files')
]
