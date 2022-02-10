#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: leeyoshinari

import os
import configparser


cfg = configparser.ConfigParser()
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(path, 'config.conf')
cfg.read(config_path, encoding='utf-8')


def getConfig(key):
	return cfg.get('default', key, fallback=None)


def get_ip():
	"""
	获取当前服务器IP地址
	:return: IP
	"""
	try:
		result = os.popen("hostname -I").readlines()
		IP = result[0].split(' ')[0].strip()
	except:
		IP = '127.0.0.1'

	return IP
