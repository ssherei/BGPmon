#!/usr/bin/python

import socket
import argparse
import MySQLdb as mysql
import smtplib
import email.utils
from email.mime.text import MIMEText
import sys
import cStringIO



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
			self.table = 'base_line'
			self.cur = self.conn.cursor()
				
			self.cur.execute('select * from %s where IP = (select id from watched where network = %%s)' % self.table (self.IP))
			if not self.cur.fetchone():
				self.cur.execute('insert into %s (network) values (select id from watched where network = %%s)' % self.table, (self.IP))
			self.conn.commit()	
		
		else:
			self.table = 'latest_update'
                        self.cur = self.conn.cursor()

			print '[*] Adding Entry to latest_update'
                        self.cur.execute('insert into %s (network,Origin_AS,IP,BGP_prefix,CC,Registry,Allocated,AS_Name) values ((select id from watched where network like %%s),%%s,%%s,%%s,%%s,%%s,%%s,%%s)' % self.table, (self.IP,self.origin_AS,self.IP,self.BGP_prefix,self.CC,self.Registry,self.Allocated,self.AS_name))
                        self.conn.commit()
			
			
		self.cur.close()


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
		self.reply = cStringIO.StringIO(self.reply)
		self.reply = self.reply.readlines()
		for self.item in self.reply[1:]:
			self.data = self.item.split('|')
			self.origin_AS  = self.data[0].strip()
			self.IP  = self.data[1].strip()
			self.BGP_prefix = self.data[2].strip()
			self.CC = self.data[3].strip()
			self.Registry = self.data[4].strip()
			self.Allocated = self.data[5].strip()
			self.AS_name = self.data[6].strip()
			print """
Origin AS: %s
IP: %s
BGP_prefix: %s
CC: %s
Registr: %s
Allocated: %s
AS_name: %s""" % (self.origin_AS,self.IP,self.BGP_prefix,self.CC,self.Registry,self.Allocated,self.AS_name)
			if b:
				self.sql_populate(b)
			else:
				self.sql_populate()
		self.conn.close()

c  = start()
c.magic()	

