#!/usr/bin/python


import time
import datetime
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from urlparse import urljoin
import json
import mysql.connector

edgerc = EdgeRc('/root/.edgerc')
section = 'bamreport'
baseurl = 'https://%s' % edgerc.get(section, 'host')
s = requests.Session()
s.auth = EdgeGridAuth.from_edgerc(edgerc, section)

short_contractId = "XXXXXX"
contractId = "ctr_" + short_contractId

short_groupId = "111111"
groupId = "grp_" + short_groupId


## Get all CP Codes for AMD on Above group ID
endurl = "/papi/v1/cpcodes?contractId=" + contractId + "&groupId=" + groupId
result = s.get(urljoin(baseurl, endurl))
cpcodes = result.json()
string = ""
for deets in cpcodes['cpcodes']['items']:
	cpcode =  deets['cpcodeId']
	for i in range(len(deets['productIds'])):
		if "Adaptive" in str(deets['productIds'][i]):
			string = string + "," + cpcode[4:]
cpcodelist = string[1:]


cnx = mysql.connector.connect(user='bamtech', password='password',
                              host='1.1..1',
                              database='bamtech')

endurl = "/media-delivery-reports/v1/adaptive-media-delivery/data?dimensions=1%2C2%2C5&metrics=15%2C5&startDate=2018-09-08T15:30Z&endDate=2018-09-10T15:30Z&&offset=0&aggregation=day&cpcodes=" + cpcodelist
result = s.get(urljoin(baseurl, endurl))
output = result.json()
insert = ""
columns = ""
for items in output['columns']:
        name = str(items['name'])
        name = name.replace(" ", "_")
        name = name.replace("/", "_")
        columns = columns + "," + name
        namesql = name + " varchar(800)"
        insert  = insert + "," + namesql
insert = insert[1:]
columns = columns[1:]

insert = "CREATE TABLE IF NOT EXISTS bamtech (" + insert + ");"
cursor = cnx.cursor()

cursor.execute(insert)
for items in output['rows']:
	zero =str(items[0])
	one = str(items[1])
	two = str(items[2])
	three = str(items[3])
	four = str(items[4])
	statement = "INSERT INTO bamtech (" + columns + ") VALUES ( %s, %s, %s, %s, %s)"
	cursor.execute(statement, (zero, one, two, three, four))
	cnx.commit()
cnx.close()
exit(0)
