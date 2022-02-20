#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
from django.urls import path
from . import views

app_name = 'myfiles'
urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('', views.home, name='home'),
    path('folder/get', views.get_folders_by_id, name='get_folder'),
    path('folder/create', views.create_folder, name='create_folder'),
    path('folder/rename', views.rename_folder, name='rename_folder'),
    path('folder/delete', views.delete_folder, name='delete_folder'),
    path('folder/getPath', views.find_origin_path, name='find_origin_path'),
    path('folder/return', views.return_last_path, name='return_folder'),
    path('folder/move', views.move_to_folder, name='move_folder'),
    path('folder/export', views.export_folder, name='move_folder'),
    path('file/get', views.get_all_files, name='get_all_files'),
    path('file/upload', views.upload_file, name='upload_file'),
    path('file/download', views.download_file, name='download_file'),
    path('file/multiple/download', views.download_multiple_file, name='download_multiple_files'),
    path('file/get/recent', views.get_recent_files, name='get_recent_files'),
    path('file/search', views.search_file, name='search_file'),
    path('file/rename', views.rename_file, name='rename_file'),
    path('file/delete', views.delete_file, name='delete_file'),
    path('file/share', views.share_file, name='share_file'),
    path('file/getShare', views.get_share_file, name='get_share_file'),
    path('file/getByFormat', views.get_file_by_format, name='get_files_format'),
    path('file/garbage', views.get_garbage, name='get_garbage'),
    path('file/recovery', views.recovery_file_from_garbage, name='recovery_file'),
    path('file/history', views.get_history, name='get_history'),
    path('open', views.open_share_file, name='open_share_file'),

    path('md/view', views.md_view, name='md_view')
]
