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

short_groupId = "11111"
groupId = "grp_" + short_groupId


## Print all data store info -- For info only.
print "Below is available data from AMD API... \n\n"
endurl = "/media-delivery-reports/v1/adaptive-media-delivery/data-stores"
result = s.get(urljoin(baseurl, endurl))
groups1 = result.json()
for items1 in groups1:
	print "Bucket ID " + str(items1['id'])
	print "Bucket Name " + str(items1['name'])
	print "Bucket Description " + str(items1['description'])
	id = items1['id']
	endurl = "/media-delivery-reports/v1/adaptive-media-delivery/data-stores/"+ str(id)
	result = s.get(urljoin(baseurl, endurl))
	print "\nRaw Output\n"
	print result.text
	print "\nParsed Output\n"
	groups2 = result.json()
	for thing in groups2['dimensions']:
		print "\t\tDimension ID " + str(thing['id'])
		print "\t\tDimension Name " + str(thing['name'])
	for thing in groups2['metrics']:
		print "\t\t Metric ID " + str(thing['id'])
		print "\t\t Metric Name " + str(thing['name'])


exit(0)
