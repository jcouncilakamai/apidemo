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

## Pull report . Replace dimensions/metrics from above printout and/or edit dates below

print "\n\n\n\n"
endurl = "/media-delivery-reports/v1/adaptive-media-delivery/data?dimensions=1%2C2%2C5&metrics=15%2C5&startDate=2018-09-08T15:30Z&endDate=2018-09-10T15:30Z&&offset=0&aggregation=day&cpcodes=" + cpcodelist
result = s.get(urljoin(baseurl, endurl))
print result.text
exit(0)
