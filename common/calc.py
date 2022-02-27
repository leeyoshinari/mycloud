#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import hashlib


def calc_md5(f):
	myhash = hashlib.md5()
	while True:
		b = f.read(8096)
		if not b:
			break
		myhash.update(b)
	return myhash.hexdigest()


def calc_file_md5(file_path):
	with open(file_path, 'rb') as f:
		res = calc_md5(f)
	return res

def beauty_size(size):
	size = size / 1024
	if size < 1000:
		return f'{round(size, 2)} KB'
	else:
		size = size / 1024
	if size < 1000:
		return f'{round(size, 2)} MB'
	else:
		return f'{round(size / 1024, 2)} GB'


if __name__ == '__main__':
	print(beauty_size(1150477982))
	print(calc_file_md5('config.py'))
