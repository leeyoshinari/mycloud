#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import os
import time
import json
import random
import logging
import zipfile
import traceback
from django.shortcuts import render
from django.core import serializers
from django.contrib import auth
from django.http import StreamingHttpResponse
from django.db.models.deletion import ProtectedError
from .models import Catalog, Files, History, Delete, Shares
from common.Results import result
from common.Messages import Msg
from common.md5 import calc_md5
from common.MinioStorage import MinIOStorage


storage = MinIOStorage()
formats = {'image': ['jpg', 'jpeg', 'bmp', 'png'], 'video': ['mp4', 'avi'], 'document': ['txt', 'md'],
           'docx': ['docx'], 'xlsx': ['xlsx'], 'pptx': ['pptx'], 'pdf': ['pdf'], 'music': ['mp3']}
content_type = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'bmp': '', 'png': '', 'pdf': 'application/pdf',
                'mp4': 'video/mp4', 'zip': 'application/zip'}


def login(request):
    if request.method == 'POST':
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            ip = request.headers.get('x-real-ip')
            session = auth.authenticate(username=username, password=password)
            if session:
                auth.login(request, session)
                request.session.set_expiry(3600)
                History.objects.create(file_id=-1, file_name=username, operate='login', ip=ip,
                                       operate_time=time.strftime('%Y-%m-%d %H:%M:%S'))
                return result(msg=Msg.MsgLonginSuccess)
            else:
                return result(code=1, msg=Msg.MsgLonginFailure)
        else:
            return result(code=1, msg=Msg.MsgParamError)
    else:
        return render(request, 'login.html')


def logout(request):
    username = request.user.username
    ip = request.headers.get('x-real-ip')
    auth.logout(request)
    History.objects.create(file_id=-1, file_name=username, operate='logout', ip=ip,
                           operate_time=time.strftime('%Y-%m-%d %H:%M:%S'))
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


def upload_file(request):
    if request.method == 'POST':
        form = request.FILES['file']
        file_name = form.name
        file_size = form.size
        parent_id = request.POST.get('parent_id')
        content_type = form.content_type
        data = form.file
        md5 = calc_md5(data)
        try:
            file = Files.objects.get(md5=md5)
            return result(code=2, msg=Msg.MsgFastUploadSuccess, data=file.name)
        except Files.DoesNotExist:
            data.seek(0)
        random_i = int(time.time() * 100) % 100
        bucket_name = str((500 + random_i * 5) ^ (2521 - random_i * 2))
        object_name = str(random.randint(1, 99)) + str(int(time.time())) + '.' + file_name.split('.')[-1]
        res = storage.upload_file_bytes(bucket_name, object_name, data, file_size, content_type=content_type)
        if res:
            try:
                file_id = str(random.randint(1000, 9999)) + str(int(time.time()))
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                Files.objects.create(id=file_id, name=file_name, origin_name=file_name, format=file_name.split('.')[-1],
                                            parent_id=parent_id, path=f'{bucket_name}/{res.object_name}',
                                            size=file_size, md5=md5, create_time=current_time, update_time=current_time)
                return result(msg=Msg.MsgUploadSuccess, data=file_name)
            except Exception as err:
                logging.error(err)
                logging.error(traceback.format_exc())
                storage.delete_file(bucket_name, res.object_name)
                return result(code=1, msg=Msg.MsgUploadFailure, data=file_name)
        else:
            return result(code=1, msg=Msg.MsgUploadFailure, data=file_name)


def download_file(request):
    if request.method == 'GET':
        try:
            file_id = request.GET.get('id')
            file = Files.objects.get(id=file_id)
            object_file = file.path.split('/')
            response = StreamingHttpResponse(storage.download_bytes(object_file[0], object_file[-1]))
            response['Content-Type'] = content_type[file.format]
            response['Content-Disposition'] = f'attachment;filename="{file.name}"'
            return response
        except Exception as err:
            logging.error(f'Download file failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgDownloadFailure, data=file_id)


def download_multiple_file(request):
    if request.method == 'GET':
        try:
            file_ids = request.GET.get('id')
            file_list = file_ids.split(',')
            files = Files.objects.filter(id__in=file_list)
            zip_multiple_file(files)
            response = StreamingHttpResponse(open('temp/temp.zip', 'rb'))
            response['Content-Type'] = 'application/zip'
            response['Content-Disposition'] = 'attachment;filename="download.zip"'
            return response
        except Exception as err:
            logging.error(f'Download multiple files failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgDownloadFailure)


def export_folder(request):
    if request.method == "GET":
        try:
            folder_id = request.GET.get('id')
            files = Files.objects.filter(parent_id=folder_id)
            if len(files) < 1:
                return result(code=1, msg=Msg.MsgExportError)
            folder_name = files[0].parent.name
            zip_multiple_file(files)
            response = StreamingHttpResponse(open('temp/temp.zip', 'rb'))
            response['Content-Type'] = 'application/zip'
            response['Content-Disposition'] = f'attachment;filename="{folder_name}.zip"'
            return response
        except Exception as err:
            logging.error(f'Export folder failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgDownloadFailure)


def rename_file(request):
    if request.method == 'POST':
        try:
            file_id = request.POST.get('id')
            file_name = request.POST.get('name')
            file = Files.objects.get(id=file_id)
            file_list = file.name.split('.')
            if file_name == file_list[0]:
                return result(msg=Msg.MsgRenameSuccess)
            file.name = f'{file_name}.{file_list[-1]}'
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
    if request.method == 'POST':
        try:
            file_id = request.POST.get('file_id')
            is_delete = request.POST.get('type')
            host = request.headers.get('x-real-ip')
            file_list = file_id.split(',')
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            if is_delete == '0':
                files = Files.objects.filter(id__in=file_list)
                for file in files:
                    Delete.objects.create(id=file.id, name=file.name, origin_name=file.origin_name, format=file.format,
                                          parent_id=file.parent_id, path=file.path, size=file.size, md5=file.md5,
                                          create_time=file.create_time, update_time=file.update_time, delete_time=current_time)
                files.delete()
            if is_delete == '1':
                files = Delete.objects.filter(id__in=file_list)
                for file in files:
                    path = file.path.split('/')
                    History.objects.create(file_id=file.id, file_name=file.name, operate='delete', operate_time=current_time, ip=host)
                    storage.delete_file(path[0], path[-1])
                    file.delete()
            if is_delete == '9':
                files = Delete.objects.all()
                for file in files:
                    path = file.path.split('/')
                    History.objects.create(file_id=file.id, file_name=file.name, operate='delete', operate_time=current_time, ip=host)
                    storage.delete_file(path[0], path[-1])
                    file.delete()
            if is_delete == '6':
                Shares.objects.get(id=file_id).delete()
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
            file_count = Files.objects.filter(format__in=formats[file_format]).count()
            files = Files.objects.filter(format__in=formats[file_format]).order_by(order_type)[(page_num - 1) * page_size: page_num * page_size]
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
                Catalog.objects.filter(id=from_id).update(parent_id = to_id, update_time = time.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                file_list = from_id.split(',')
                Files.objects.filter(id__in=file_list).update(parent_id = to_id, update_time = time.strftime('%Y-%m-%d %H:%M:%S'))

            return result(msg=Msg.MsgMoveSuccess)
        except Exception as err:
            logging.error(f'Move file failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgMoveFailure)


def get_garbage(request):
    if request.method == 'GET':
        try:
            page_num = request.GET.get('page')
            page_num = int(page_num) if page_num else 1
            total_num = Delete.objects.all().count()
            files = Delete.objects.all().order_by('-delete_time')[(page_num - 1) * 20: page_num * 20]
            return result(msg=Msg.MsgGetFileSuccess, data={'data': json.loads(serializers.serialize('json', files)),
                                                           'total_page': total_num // 20 + 1, 'page': page_num})
        except Exception as err:
            logging.error(f'Get garbage error: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgGetFileFailure)


def recovery_file_from_garbage(request):
    if request.method == 'GET':
        try:
            file_ids = request.GET.get('id')
            file_list = file_ids.split(',')
            files = Delete.objects.filter(id__in=file_list)
            for file in files:
                Files.objects.create(id=file.id, name=file.name, origin_name=file.origin_name, format=file.format,
                              parent_id=file.parent_id, path=file.path, size=file.size, md5=file.md5,
                              create_time=file.create_time, update_time=file.update_time)
            files.delete()
            return result(msg=Msg.MsgOperateSuccess)
        except Exception as err:
            logging.error(f'Recovery file from garbage error: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgOperateFailure)


def zip_multiple_file(file_list):
    archive = zipfile.ZipFile('temp/temp.zip', 'w', zipfile.ZIP_DEFLATED)
    for file in file_list:
        object_file = file.path.split('/')
        storage.save_file(object_file[0], object_file[-1], file.name)
        archive.write('temp/' + file.name, file.name)
        os.remove('temp/' + file.name)
    archive.close()


def share_file(request):
    if request.method == 'POST':
        try:
            file_id = request.POST.get('file_id')
            times = request.POST.get('times')
            times = int(times) if times else 5
            file = Files.objects.get(id=file_id)
            Shares.objects.create(id=int(time.time()) % 10000, file_id=file.id, name=file.name, path=file.path, format=file.format,
                                  times=0, total_times=times, create_time=time.strftime('%Y-%m-%d %H:%M:%S'))
            return result(msg=Msg.MsgShareSuccess)
        except Exception as err:
            logging.error(f'Share file failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgShareFailure)


def get_share_file(request):
    if request.method == 'GET':
        try:
            files = Shares.objects.all().order_by('-create_time')
            return result(msg=Msg.MsgGetFileSuccess, data=json.loads(serializers.serialize('json', files)))
        except Exception as err:
            logging.error(f'Get files error: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgGetFileFailure)


def open_share_file(request):
    if request.method == 'GET':
        try:
            share_id = request.GET.get('id')
            host = request.headers.get('x-real-ip')
            share = Shares.objects.get(id=share_id)
            History.objects.create(file_id=share.file_id, file_name=share.name, operate='openShare',
                                   operate_time=time.strftime('%Y-%m-%d %H:%M:%S'), ip=host)
            if share.times < share.total_times:
                path = share.path.split('/')
                response = StreamingHttpResponse(storage.download_bytes(path[0], path[-1]))
                response['Content-Type'] = content_type[share.format]
                response['Content-Disposition'] = f'inline;filename="{share.name}"'
                share.times = share.times + 1
                share.save()
                return response
            else:
                return render(request, '404.html')
        except Exception as err:
            logging.error(f'Open share file failure: {err}')
            return render(request, '404.html')


def get_history(request):
    if request.method == 'GET':
        try:
            page_num = request.GET.get('page')
            page_num = int(page_num) if page_num else 1
            total_num = History.objects.all().count()
            hostory = History.objects.all().order_by('-operate_time')[(page_num - 1) * 20: page_num * 20]
            return result(msg=Msg.MsgGetFileSuccess, data={'data': json.loads(serializers.serialize('json', hostory)),
                                                       'total_page': total_num // 20 + 1, 'page': page_num})
        except Exception as err:
            logging.error(f'Get garbage error: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgGetFileFailure)


def md_view(request):
    if request.method == 'GET':
        try:
            file_id = request.GET.get('id')
            file = Files.objects.get(id=file_id)
            path = file.path.split('/')
            res = storage.download_bytes(path[0], path[-1])
            return render(request, 'editorMD.html', context={'content': res.data.decode(), 'name': file.name})
        except Exception as err:
            logging.error(f'Get md file failure: {err}')
            logging.error(traceback.format_exc())
            return render(request, '404.html')


def get_md_file_id(request):
    if request.method == 'GET':
        try:
            file_id = request.GET.get('id')
            file = Files.objects.get(id=file_id)
            path = file.path.split('/')
            data = storage.download_bytes(path[0], path[-1])
            return result(msg=Msg.MsgGetFileSuccess, data={'data': data.data.decode(), 'name': file.name})
        except Exception as err:
            logging.error(f'Get file failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgGetFileFailure)
