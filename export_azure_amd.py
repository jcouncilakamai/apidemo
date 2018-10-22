#!/usr/bin/python


import time
import datetime
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from urlparse import urljoin
import json
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

edgerc = EdgeRc('/root/.edgerc')
section = 'bamreport'
baseurl = 'https://%s' % edgerc.get(section, 'host')
s = requests.Session()
s.auth = EdgeGridAuth.from_edgerc(edgerc, section)

short_contractId = "X-XXXXX"
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
myaccount = "bamtechtesting"
accountkey = "XXXXX"
table_service = TableService(account_name=myaccount, account_key=accountkey)
table_name = "tablename"
table_service.create_table(table_name)


endurl = "/media-delivery-reports/v1/adaptive-media-delivery/data?dimensions=1%2C2%2C5&metrics=15%2C5&startDate=2018-09-08T15:30Z&endDate=2018-09-10T15:30Z&&offset=0&aggregation=day&cpcodes=" + cpcodelist
result = s.get(urljoin(baseurl, endurl))
output = result.json()
insert = ""
columns = ""
czero = output['columns'][0]['name']
cone = output['columns'][1]['name']
ctwo = output['columns'][2]['name']
ctwo = ctwo.replace(" ", "_")
ctwo = ctwo.replace("/", "_")

cthree = output['columns'][3]['name']
cthree = cthree.replace(" ", "_")
cthree = cthree.replace("/", "_")

cfour = output['columns'][4]['name']
cfour = cfour.replace(" ", "_")
number = 0
for items in output['rows']:
	zero =str(items[0])
	one = str(items[1])
	two = str(items[2])
	three = str(items[3])
	four = str(items[4])
	number = number +1
	snum  = str(number)
	snum = snum.zfill(2)
	print snum
	log = {'PartitionKey': 'bamtechlogs', 'RowKey': snum, czero : zero, cone : one, ctwo : two , cthree : three, cfour : four}
	table_service.insert_entity(table_name, log)

exit(0)
