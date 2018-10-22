#!/usr/bin/python


import time
import datetime
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from urlparse import urljoin
import json
import xlsxwriter

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


print "\n\n\n\n"
print "Results from pull are in report.xlsx in this directory ...\n\n\n\n"
endurl = "/media-delivery-reports/v1/adaptive-media-delivery/data?dimensions=1%2C2%2C5&metrics=15%2C5&startDate=2018-09-08T15:30Z&endDate=2018-09-10T15:30Z&&offset=0&aggregation=day&cpcodes=" + cpcodelist
result = s.get(urljoin(baseurl, endurl))
output = result.json()
workbook = xlsxwriter.Workbook('report.xlsx')
date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
worksheet = workbook.add_worksheet("AMD Report for " + groupId)
bold = workbook.add_format({'bold': True, 'font_size' : "14"})
digit = 0
worksheet.set_column(0, 6, 25)
worksheet.autofilter('A1:D1000')
for items in output['columns']:
	char = chr(ord('a') + digit)
	cell = str(char) + "1"
	cell = cell.upper()
	name = str(items['name'])
	description = str(items['description'])
	worksheet.write(cell,name,bold)
	worksheet.write_comment(cell,description)
	digit  = digit +1
digit = 2
for items in output['rows']:
	item = float(items[0])
	value = datetime.datetime.fromtimestamp(item).strftime('%Y-%m-%d %H:%M:%S')
	cell = "A" + str(digit)
	worksheet.write(cell,value)
	item = str(items[1])
	cell = "B" + str(digit)
	worksheet.write(cell,item)
	item = str(items[2])
	cell = "C" + str(digit)
	worksheet.write(cell,item)
	item = str(items[3])
	cell = "D" + str(digit)
	worksheet.write(cell,item)
	item = str(items[4])
	cell = "E" + str(digit)
	worksheet.write(cell,item)
	digit = digit +1
workbook.close()
exit(0)
