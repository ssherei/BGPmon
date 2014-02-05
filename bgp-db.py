import MySQLdb as mysql
import sys

try:
	conn = mysql.connect('localhost','bgpmon','bgpmon','bgpmon')
	with conn:
		
		print "[*] Creating table watched"
		cur = conn.cursor()
		cur.execute("drop table if exists watched")
		cur.execute("create table watched (id int primary key auto_increment, network varchar(100), time_stamp timestamp)")

		print "[*] Creating Table base_line"
		cur.execute("drop table if exists base_line")
		cur.execute("create table base_line (id int primary key auto_increment, network int, Origin_AS int,  IP varchar(100), BGP_prefix varchar(100), CC varchar(5), Registry varchar(25), Allocated datetime, AS_Name varchar(300), time_stamp timestamp, constraint fk_IP foreign key (network) references watched(id) on update cascade on delete cascade)") 

		print "[*] Creating Table latest_update"
                cur.execute("drop table if exists latest_update")
                cur.execute("create table latest_update (id int primary key auto_increment, network int, Origin_AS int,  IP varchar(100), BGP_prefix varchar(100), CC varchar(5), Registry varchar(25), Allocated datetime, AS_Name varchar(300), time_stamp timestamp, constraint fk_IP_latest foreign key (network) references watched(id) on update cascade on delete cascade)")

		print "[*] Creating Table emails"
                cur.execute("drop table if exists emails")
                cur.execute("create table emails(id int primary key auto_increment, email varchar(100)")

		print "[*] Creating Table Validate"
		cur.execute("drop table if exists validate")
		cur.execute("create table validate(id int primary key auto_increment, network varchar(50), diff_type varchar(50), diff_rec varchar(1024), time_stamp timestamp)")


print "[*] Creating Table Alert_history"
cur.execute("drop table if exists alert_hitory")
cur.execute("create table alert_history (id int primary key auto_increment, network varchar(50), diff_type varchar(50), diff_rec varchar(1024), time_stamp timestamp)")



except mysql.Error, e:
	
	print "[*] Error %d, %s" % (e.args[0], e.args[1])
	sys.exit(1)


