#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import time
import json
import random
import logging
import traceback
from django.shortcuts import render
from django.core import serializers
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from .models import Catalog, Files, History
from common.Results import result
from common.Messages import Msg


def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def create_folder(request):
    if request.method == 'POST':
        try:
            file_name = request.POST.get('name')
            parent_id = request.POST.get('id')
            file_id = str(random.randint(1000, 9999)) + str(int(time.time()))
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            folder = Catalog.objects.create(id=file_id, parent_id=parent_id, name=file_name,
                                            create_time=current_time, update_time=current_time)
            logging.info(f'Create Folder success, Folder-id-name: {folder.id},{folder.name}')
            return result(msg=Msg.MsgCreateSuccess.format(folder.name))
        except Exception as err:
            logging.info(f'Create Folder failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgCreateFailure)


def rename_folder(request):
    if request.method == 'POST':
        try:
            folder_id = request.POST.get('id')
            folder_name = request.POST.get('name')
            folder = Catalog.objects.get(id=folder_id)
            if folder.name == folder_name:
                return result(msg=Msg.MsgRenameSuccess)
            folder.name = folder_name
            folder.update_time = time.strftime('%Y-%m-%d %H:%M:%S')
            folder.save()
            return result(msg=Msg.MsgRenameSuccess)
        except Exception as err:
            logging.error(f'Rename folder failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgRenameFailure)


def rename_file(request):
    if request.method == 'POST':
        try:
            file_id = request.POST.get('id')
            file_name = request.POST.get('name')
            file = Files.objects.get(id=file_id)
            if file.name == file_name:
                return result(msg=Msg.MsgRenameSuccess)
            file.name = file_name
            file.update_time = time.strftime('%Y-%m-%d %H:%M:%S')
            file.save()
            return result(msg=Msg.MsgRenameSuccess)
        except Exception as err:
            logging.error(f'Rename folder failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgRenameFailure)


def delete_folder(request):
    if request.method == 'GET':
        try:
            folder_id = request.GET.get('id')
            Catalog.objects.get(id=folder_id).delete()
            Catalog.objects.filter(parent_id=folder_id).delete()
            logging.info(f'Delete Folder success, Folder-id: {folder_id}')
            return result(msg=Msg.MsgDeleteSuccess)
        except ProtectedError as err:
            logging.error(f'Delete Folder failure: {err}')
            return result(code=2, msg=Msg.MsgProtectedError)
        except Exception as err:
            logging.error(f'Delete Folder failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgDeleteFailure)


def delete_file(request):
    if request.method == 'GET':
        try:
            file_id = request.GET.get('id')
            Files.objects.get(id=file_id).delete()
            logging.info(f'Delete Folder success, File-id: {file_id}')
            return result(msg=Msg.MsgDeleteSuccess)
        except Exception as err:
            logging.error(f'Delete Folder failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgDeleteFailure)


def get_recent_files(request):
    if request.method == 'GET':
        try:
            page_size = request.GET.get('page')
            page_size = int(page_size) if page_size else 20
            recent_file = Files.objects.filter().order_by('-update_time')[0: page_size]
            return result(data=json.loads(serializers.serialize('json', recent_file)), msg=Msg.MsgGetFileSuccess)
        except Exception as err:
            logging.error(f'Get recent files failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgGetFileFailure)


def get_all_files(request):
    """获取目录下的所有文件"""
    if request.method == 'POST':
        try:
            folder_id = request.POST.get('id')
            page_num = request.POST.get('page')
            page_size = request.POST.get('page_size')
            page_num = int(page_num) if page_num else 1
            page_size = int(page_size) if page_size else 20
            sorted = request.POST.get('sorted')
            sorted_type = request.POST.get('sorted_type')
            order_type = f'-{sorted_type}' if sorted == 'desc' else f'{sorted_type}'
            folder_count = Catalog.objects.filter(parent_id=folder_id).count()
            file_count = Files.objects.filter(parent_id=folder_id).count()
            offset_page = folder_count // page_size
            offset_num = folder_count % page_size
            if (page_num - 1) < offset_page:
                if sorted_type == 'format' or sorted_type == 'size':
                    folders = Catalog.objects.filter(parent_id=folder_id).order_by('-update_time')[(page_num - 1) * page_size: page_num * page_size]
                else:
                    folders = Catalog.objects.filter(parent_id=folder_id).order_by(order_type)[(page_num - 1) * page_size: page_num * page_size]
                all_files = json.loads(serializers.serialize('json', folders))
            elif (page_num - 1) == offset_page:
                if sorted_type == 'format' or sorted_type == 'size':
                    folders = Catalog.objects.filter(parent_id=folder_id).order_by('-update_time')[(page_num - 1) * page_size: page_num * page_size]
                else:
                    folders = Catalog.objects.filter(parent_id=folder_id).order_by(order_type)[(page_num - 1) * page_size: page_num * page_size]
                files = Files.objects.filter(parent_id=folder_id).order_by(order_type)[(page_num - 1 - offset_page) * page_size: (page_num - offset_page) * page_size - offset_num]
                folders_json = json.loads(serializers.serialize('json', folders))
                files_json = json.loads(serializers.serialize('json', files))
                all_files = folders_json + files_json
            else:
                files = Files.objects.filter(parent_id=folder_id).order_by(order_type)[(page_num - 1 - offset_page) * page_size - offset_num: (page_num - offset_page) * page_size - offset_num]
                all_files = json.loads(serializers.serialize('json', files))

            return result(data={'data': all_files, 'total_page': (folder_count + file_count) // page_size + 1, 'page': page_num}, msg=Msg.MsgGetFileSuccess)
        except Exception as err:
            logging.error(f'Get files error: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgGetFileFailure)


def search_file(request):
    if request.method == 'POST':
        try:
            key_word = request.POST.get('key_word')
            key_word = key_word.strip().replace('%', '')
            if not key_word:
                return result(code=0, msg=Msg.MsgGetFileSuccess)
            page_num = request.POST.get('page')
            page_size = request.POST.get('page_size')
            page_num = int(page_num) if page_num else 1
            page_size = int(page_size) if page_size else 20
            folder_count = Catalog.objects.filter(name__contains=key_word).count()
            file_count = Files.objects.filter(name__contains=key_word).count()
            offset_page = folder_count // page_size
            offset_num = folder_count % page_size
            if (page_num - 1) < offset_page:
                folders = Catalog.objects.filter(name__contains=key_word).order_by('-update_time')[(page_num - 1) * page_size: page_num * page_size]
                all_files = json.loads(serializers.serialize('json', folders))
            elif (page_num - 1) == offset_page:
                folders = Catalog.objects.filter(name__contains=key_word).order_by('-update_time')[(page_num - 1) * page_size: page_num * page_size]
                files = Files.objects.filter(name__contains=key_word).order_by('-update_time')[(page_num - 1 - offset_page) * page_size: (page_num - offset_page) * page_size - offset_num]
                folders_json = json.loads(serializers.serialize('json', folders))
                files_json = json.loads(serializers.serialize('json', files))
                all_files = folders_json + files_json
            else:
                files = Files.objects.filter(name__contains=key_word).order_by('-update_time')[(page_num - 1 - offset_page) * page_size - offset_num: (page_num - offset_page) * page_size - offset_num]
                all_files = json.loads(serializers.serialize('json', files))

            return result(data={'data': all_files, 'total_page': (folder_count + file_count) // page_size + 1, 'page': page_num}, msg=Msg.MsgGetFileSuccess)
        except Exception as err:
            logging.error(f'Search file failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgGetFileFailure)


def find_origin_path(request):
    if request.method == 'GET':
        try:
            folder_id = request.GET.get('id')
            all_path = []
            folder = Catalog.objects.get(id=folder_id)
            all_path.append(folder.name)
            parent_id = folder.parent_id
            if folder_id == '520':
                return result(msg=Msg.MsgGetFileSuccess, data='当前文件在根目录')
            while parent_id != '520':
                folder = Catalog.objects.get(id=parent_id)
                all_path.append(folder.name)
                parent_id = folder.parent_id
            all_path.reverse()
            return result(msg=Msg.MsgGetFileSuccess, data=' > '.join(all_path))
        except Exception as err:
            logging.error(f'Find origin path failure: {folder_id}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgGetFileFailure)


def return_last_path(request):
    if request.method == 'GET':
        try:
            folder_id = request.GET.get('id')
            folder_name = request.GET.get('name')
            parent_id = Catalog.objects.get(id=folder_id).parent_id
            if parent_id == '520':
                folder_name = ''
            else:
                folder_list = folder_name.split(' > ')
                folder_list.pop(-1)
                folder_name = ' > '.join(folder_list)
            return result(msg=Msg.MsgOperateSuccess, data={'id': parent_id, 'name': folder_name})
        except Exception as err:
            logging.error(f'Return last path failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgOperateFailure)


def get_file_by_format(request):
    if request.method == 'POST':
        try:
            file_format = request.POST.get('format')
            page_num = request.POST.get('page')
            page_size = request.POST.get('page_size')
            page_num = int(page_num) if page_num else 1
            page_size = int(page_size) if page_size else 20
            sorted = request.POST.get('sorted')
            sorted_type = request.POST.get('sorted_type')
            order_type = f'-{sorted_type}' if sorted == 'desc' else f'{sorted_type}'
            file_count = Files.objects.filter(format=file_format).count()
            files = Files.objects.filter(format=file_format).order_by(order_type)[(page_num - 1) * page_size: page_num * page_size]
            all_files = json.loads(serializers.serialize('json', files))
            return result(data={'data': all_files, 'total_page': file_count // page_size + 1, 'page': page_num}, msg=Msg.MsgGetFileSuccess)
        except Exception as err:
            logging.error(f'Find files of format "{file_format}" failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgGetFileFailure)


def get_folders_by_id(request):
    if request.method == 'GET':
        try:
            folder_id = request.GET.get('id')
            folders = Catalog.objects.filter(parent_id=folder_id)
            return result(data=json.loads(serializers.serialize('json', folders)), msg=Msg.MsgGetFileSuccess)
        except Exception as err:
            logging.error(f'Find folders by id-{folder_id} failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgGetFileFailure)


def move_to_folder(request):
    if request.method == 'POST':
        try:
            from_id = request.POST.get('from_id')
            to_id = request.POST.get('to_id')
            move_type = request.POST.get('move_type')
            if move_type == 'folder':
                folder = Catalog.objects.get(id=from_id)
                folder.parent_id = to_id
                folder.update_time = time.strftime('%Y-%m-%d %H:%M:%S')
                folder.save()
            if move_type == 'file':
                file = Files.objects.get(id=from_id)
                file.parent_id = to_id
                file.update_time = time.strftime('%Y-%m-%d %H:%M:%S')
                file.save()

            return result(msg=Msg.MsgMoveSuccess)
        except Exception as err:
            logging.error(f'Move file failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgMoveFailure)

