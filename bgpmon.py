#!/usr/bin/python

import socket
import argparse
import MySQLdb as mysql
import smtplib
import email.utils
from email.mime.text import MIMEText
import sys




class start():
	
	def __init__(self):
		self.db_host = 'localhost'
		self.db_user = 'bgpmon'
		self.db_pass = 'bgpmon'
		self.db = 'bgpmon'
		self.fd = open('/var/log/bgpmon','a')
		pass

	def sql_conn(self):
		try:
			self.conn = mysql.connect(self.db_host,self.db_user,self.db_pass,self.db)
	
		except mysql.Error, self.e:
	
			print "Error %d:%s" % (self.e.args[0], self.e.args[1])
			sys.exit(1)
	

	def sql_populate(self,b=None):
			
		if b:
			self.table = 'baseline'
			self.cur = self.conn.cursor()
			self.cur.execute('select * from %s where ip = (select id from watched where network = %%s' % self.table)
	
	def magic(self, b=None):

		self.sql_conn()
		self.cur = self.conn.cursor()
		self.cur.execute('select network from watched')
		self.buffer = 'begin\r\nverbose\r\nend'
		print "[*] Querying Team Cymru Whois Server for Orignating AS"
		for self.query in self.cur:
			self.index = self.buffer.index('end')
			self.buffer = self.buffer[0:self.index] + self.query[0] + '\r\n' + self.buffer[self.index:]
#			print self.buffer
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.connection.connect(('whois.cymru.com',43))
		except:
			print "[*] Communication Error"
			sys.exit(1)
		self.connection.send(self.buffer)
		self.reply = self.connection.recv(2048)
		print self.reply

c  = start()
c.magic()	

