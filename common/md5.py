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


if __name__ == '__main__':
	f = open('D:\\Code\\soulmate\\zhihu_spider\\images\\6cfb3a72803a9a61803899b41c0e672d_1.jpg', 'rb')
	print(calc_md5(f))
	f.close()
