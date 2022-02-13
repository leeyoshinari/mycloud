#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
from django.urls import path
from . import views

app_name = 'myfiles'
urlpatterns = [
    path('login', views.login, name='login'),
    path('', views.home, name='home'),
    path('folder/get', views.get_folders_by_id, name='get_folder'),
    path('folder/create', views.create_folder, name='create_folder'),
    path('folder/rename', views.rename_folder, name='rename_folder'),
    path('folder/delete', views.delete_folder, name='delete_folder'),
    path('folder/getPath', views.find_origin_path, name='find_origin_path'),
    path('folder/return', views.return_last_path, name='return_folder'),
    path('folder/move', views.move_to_folder, name='move_folder'),
    path('file/get', views.get_all_files, name='get_all_files'),
    path('file/get/recent', views.get_recent_files, name='get_recent_files'),
    path('file/search', views.search_file, name='search_file'),
    path('file/rename', views.rename_file, name='rename_file'),
    path('file/delete', views.delete_file, name='delete_file'),
    path('file/getByFormat', views.get_file_by_format, name='get_files_format')
]
