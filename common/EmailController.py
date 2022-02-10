#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: leeyoshinari

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def sendMsg(msg, logger, is_send=True):
	try:
		message = MIMEMultipart()
		if msg['smtp_server'] == 'smtp.sina.com':   # 新浪邮箱的Header不能使用utf-8的编码方式
			message['From'] = Header(msg['sender_name'])    # 发件人名字
		else:
			message['From'] = Header(msg['sender_name'], 'utf-8')
		message['To'] = Header(msg['receiver_name'], 'utf-8')       # 收件人名字
		message['Subject'] = Header(msg['subject'], 'utf-8')        # 邮件主题

		email_text = MIMEText(msg['fail_test'], 'html', 'utf-8')
		message.attach(email_text)      # 添加邮件正文

		try:
			server = smtplib.SMTP_SSL(msg['smtp_server'], 465)
		except:
			server = smtplib.SMTP(msg['smtp_server'], 25)

		server.login(msg['sender_email'], msg['password'])      # 登陆邮箱
		# server.login(msg['sender_email'], '123456')  # 登陆邮箱
		server.sendmail(msg['sender_email'], msg['receiver_email'], message.as_string())     # 发送邮件
		server.quit()
		del message
	except Exception as err:
		logger.error(err)
		if is_send:
			sendMsg(msg, logger, is_send=False)
		else:
			raise

