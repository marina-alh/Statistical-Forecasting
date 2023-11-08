import websocket
import ssl
import json

header_user = {'header_user': 'user1'}

ws = websocket.create_connection("wss://ptp-sbi01-aws-emea.sanofi.com/sense/app/", sslopt={"cert_reqs": ssl.CERT_NONE},header=header_user)

ws.send(json.dumps({
	"handle": -1,
	"method": "GetDocList",
	"params": [],
	"outKey": -1,
	"id": 1
}))

result = ws.recv()

while result:
    result=ws.recv()
    y = json.loads(result)
    print(y)

ws.close()