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

short_contractId = "XXXXX"
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

print cpcodelist
exit(0)
