BGPmon
======

BGPmon

BGP Hikack Monitoring

optional arguments:
  -h, --help            show this help message and exit
  -b, --baseline        Baseline records
  -c, --check           Check for any discrepancies in database
  -e EMAIL, --email EMAIL
                        Add Email to database
  -ip IP, --ip IP       Add IP to database

Saif El-Sherei



I. Introduction:

BGPmon monitors your bgp route for hijacking and sends email alerts whenever discrepencies is found between the baseline
and the latest update records, it utilizes "Team Cymru" IP to ASN tool using bulk queries. BGP hijack monitor grabs the 
originating AS for a list of IPs saved in the database. and if the "-b" switch is supplied will insert the result in the 
baseline table. if no switched are supplied the results will be saved in the latest Update tables.

The tool utilitzed 'Team Cymru' IP to ASN tool. i would like to extend my special appreciation and thanks to this group
for providing such a service.

II. Installation:

create database 'bgpmon' with user 'bgpmon' and password make sure to update both the bgp-db.py and bgpmon.py with 
the db name, dbhost, db user, db password.

update db details in 'bgpmon.py' line 26
update db details in 'bgp-db.py' line 5

run the bgp-db.py script to create the required tables.

add IP with '-ip' switch to be monitored

add email with '-e' swtich to be alerted


II. Usage:

since this tool is made to be running in the cli please note that all std_out is saved in the log file '/var/log/bgp_mon.log'
if you want to cancel this behaviour just comment out line 21 in 'bgpmon.py' script. you will see the output on your terminal



./bgpmon.py -e [EMAIL]

Add Email to the emails table to be alerted.

./bgpmon.py -ip [IP]

Add IP to the ips table to be monitored.

./bgpmon.py -b

grabs the origin AS for the IPs in the Database and save the results in the base_line tables

./bgpmon.py 

grabs the origin AS for the IPs in the Database and save the results in the latest_update table. and 
checks for differences between latest_update and base_line.

./bgpmon.py -c

Manual check the records with MAX time stamp in 'latest_update' table with records in the 'base_line' table 
for the each ip for differences if any difference is found send email to the saved emails.
