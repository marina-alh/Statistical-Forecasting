import requests
import websocket, ssl
import json,  csv
import os, time
from pprint import pprint 

#Connecting to the server. The lines below will be replaced by the certificates and headers for enterprise usage later
ws = websocket.WebSocket()
ws.connect("ws://localhost:4848/app/")

#For getting the doc (app) list
doclist_req = {
	"handle": -1,
	"method": "GetDocList",
	"params": [],
	"outKey": -1,
	"id": 1
}

ws.send(json.dumps(doclist_req))
result = ws.recv()
ws.send(json.dumps(doclist_req))
result = ws.recv()
result_json = json.loads(result)
print(result_json)
print()

#For opening the doc (app)
app_req = {
    "jsonrpc": "2.0",
	"method": "OpenDoc",
	"handle": -1,
	"params": [
        #Can iterate if multiple apps are there
		#Since only one app was present we used the index 0
		result_json['result']['qDocList'][0]['qDocId']
	],
	"outKey": -1,
	"id": 2
}

#The first call seems to be for establishing the connection and second to actually send the request body
ws.send(json.dumps(app_req))
result = ws.recv()
ws.send(json.dumps(app_req))
result = ws.recv()
result_json = json.loads(result)
print(result_json)
print()
app_req_handle = result_json['result']['qReturn']['qHandle']

#For creating the session object necessary for fetching dimensions, fields, etc.
session_req = {
    "jsonrpc": "2.0",
	"method": "CreateSessionObject",
	"handle": app_req_handle,
	"params": [
		{
			"qInfo": {
				"qType": "SheetList"
			},
			"qAppObjectListDef": {
				"qType": "sheet",
				"qData": {
					"title": "/qMetaDef/title",
					"description": "/qMetaDef/description",
					"thumbnail": "/thumbnail",
					"cells": "/cells",
					"rank": "/rank",
					"columns": "/columns",
					"rows": "/rows"
				}
			}
		}
	],
	"outKey": -1,
	"id": 3
}

ws.send(json.dumps(session_req))
result = ws.recv()
ws.send(json.dumps(session_req))
result = ws.recv()
result_json = json.loads(result)
print(result_json)
print()
session_req_handle = result_json['result']['qReturn']['qHandle']

#For fetching the layout of the sheets
layout_req = {
    "jsonrpc": "2.0",
    "method": "GetLayout",
    "handle": session_req_handle,
    "params": [],
    "outKey": -1,
    "id": 4
}

ws.send(json.dumps(layout_req))
result = ws.recv()
ws.send(json.dumps(layout_req))
result = ws.recv()
result_json = json.loads(result)
print(result_json)
print()

#Since only one sheet was present we used the index 0
list_of_charts = result_json['result']['qLayout']['qAppObjectList']['qItems'][0]['qData']['cells']
for chart in list_of_charts:
	print(chart['name'])
print()

ws.close()
