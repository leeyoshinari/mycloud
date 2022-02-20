#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import os
import logging
import traceback
from django.conf import settings
from minio import Minio


class MinIOStorage:
    def __init__(self, host=None, access_key=None, secret_key=None):
        self.client = None
        self.host = host if host else settings.MINIO_HOST
        self.access_key = access_key if access_key else settings.MINIO_ACCESS_KEY
        self.secret_key = secret_key if secret_key else settings.MINIO_SECRET_KEY

        self.policy = '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":' \
                      '["s3:GetBucketLocation","s3:ListBucketMultipartUploads"],"Resource":' \
                      '["arn:aws:s3:::%s"]},{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":["s3:GetObject",' \
                      '"s3:ListMultipartUploadParts","s3:PutObject","s3:AbortMultipartUpload","s3:DeleteObject"],' \
                      '"Resource":["arn:aws:s3:::%s/*"]}]}'

        self.connect_minio()
        self.init_bucket()

        if not os.path.exists('temp'):
            os.mkdir('temp')

    def connect_minio(self):
        self.client = Minio(self.host, access_key=self.access_key, secret_key=self.secret_key, secure=False)

    def init_bucket(self):
        for i in range(100):
            _ = self.create_bucket(str((500 + i * 5) ^ (2521 - i * 2)))

    def create_bucket(self, bucket_name: str):
        try:
            if self.client.bucket_exists(bucket_name):
                return f'{bucket_name} 已存在'
            self.client.make_bucket(bucket_name)
            self.client.set_bucket_policy(bucket_name, self.policy % (bucket_name, bucket_name))
            return f'{bucket_name} 创建成功'
        except Exception as err:
            logging.error(err)
            logging.error(traceback.format_exc())
            return f'{bucket_name} 创建失败'

    def upload_file_by_path(self, bucket_name: str, object_name: str, file_path: str):
        try:
            res = self.client.fput_object(bucket_name, object_name, file_path)
            return res
        except Exception as err:
            logging.error(err)
            logging.error(traceback.format_exc())
            return None

    def upload_file_bytes(self, bucket_name: str, object_name: str, data: bytes, length: int, content_type=None):
        try:
            res = self.client.put_object(bucket_name, object_name, data, length, content_type)
            return res
        except Exception as err:
            logging.error(err)
            logging.error(traceback.format_exc())
            return None

    def delete_file(self, bucket_name: str, object_names: list):
        try:
            self.client.remove_object(bucket_name, object_names)
        except Exception as err:
            logging.error(err)
            raise Exception(traceback.format_exc())

    def download_bytes(self, bucket_name: str, object_name: str):
        try:
            res = self.client.get_object(bucket_name, object_name)
            return res
        except Exception as err:
            logging.error(err)
            logging.error(traceback.format_exc())
            return None

    def save_file(self, bucket_name: str, object_name: str, file_path: str):
        try:
            res = self.client.fget_object(bucket_name, object_name, 'temp/'+ file_path)
            return res
        except Exception as err:
            logging.error(err)
            logging.error(traceback.format_exc())
            return None