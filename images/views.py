#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import time
import random
import logging
import traceback
from django.shortcuts import render
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
            parent_id = request.POST.get('parent_id')
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


def delete_folder(request):
    if request.method == 'GET':
        try:
            folder_id = request.GET.get('id')
            folder_name = request.GET.get('name')
            Catalog.objects.get(id=folder_id).delete()
            logging.info(f'Delete Folder success, Folder-id: {folder_id}')
            return result(msg=Msg.MsgDeleteSuccess.format(folder_name))
        except ProtectedError as err:
            logging.info(f'Delete Folder failure: {err}')
            return result(code=2, msg=Msg.MsgProtectedError.format(folder_name))
        except Exception as err:
            logging.info(f'Delete Folder failure: {err}')
            logging.error(traceback.format_exc())
            return result(code=1, msg=Msg.MsgDeleteFailure)

