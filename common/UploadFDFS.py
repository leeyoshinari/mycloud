#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: leeyoshinari

import os
from fdfs_client.client import Fdfs_client, get_tracker_conf


def upload_file(file_path):
    client_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'client.conf')
    client = Fdfs_client(get_tracker_conf(client_path))
    res = client.upload_by_filename(file_path)
    if res['Status'] == 'Upload successed.':
        return res['Remote file_id'].decode()
    else:
        raise Exception(res['Status'])


def upload_by_buffer(string):
    client_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'client.conf')
    client = Fdfs_client(get_tracker_conf(client_path))
    res = client.upload_by_buffer(string.encode('utf-8'), file_ext_name='log')
    if res['Status'] == 'Upload successed.':
        return res['Remote file_id'].decode()
    else:
        raise Exception(res['Status'])
