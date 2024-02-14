import asyncio
import websockets
from datetime import datetime
import json
import uuid
import time
import math
from datetime import datetime,timezone
async def run():
    id = str(uuid.uuid4())
    default_utc = "2024-01-04T23:27:02.404Z"
    
    async with websockets.connect('ws://0.0.0.0:8180/steve/websocket/CentralSystemService/testbox',
                                  subprotocols=['ocpp1.6']) as websocket:
        # await websocket.send([2,"4f3755c3-b434-4284-b5fd-d4e20514ac52","BootNotification",{"chargePointVendor":"AVT-Company","chargePointModel":"AVT-Express","chargePointSerialNumber":"avt.001.13.1","chargeBoxSerialNumber":"avt.001.13.1.01","firmwareVersion":"0.9.87","iccid":"","imsi":"","meterType":"AVT NQC-ACDC","meterSerialNumber":"avt.001.13.1.01"}])

        await websocket.send(json.dumps([2, id,
                    "BootNotification",
                    {"chargePointVendor":"AVT-Company",
                     "chargePointModel":"AVT-Express",
                     "chargePointSerialNumber":"avt.001.13.1",
                     "chargeBoxSerialNumber":"avt.001.13.1.01",
                     "firmwareVersion":"0.9.87",
                     "iccid":"",
                     "imsi":"",
                     "meterType":"AVT NQC-ACDC",
                     "meterSerialNumber":"avt.001.13.1.01"}
                     ]))
        response = await websocket.recv()

        while True:
            x = input("Enter value:\t").strip()
            if x == 'a':
                print("Authorize")

                await websocket.send(json.dumps(
                    [2,id,"Authorize",{"idTag":"1234"}]
                ))
                response = await websocket.recv()
                print(response)
            if x == 's':
                print("start charge")
                utc_time = get_utc()
                # start transaction
                await websocket.send(json.dumps(
                    [2,id,"StartTransaction",{"connectorId":1,"idTag":"1234","timestamp":utc_time,"meterStart":2,"reservationId":0}]
                ))
                response = await websocket.recv()
                print(response)
            
     
            if x == 'p':
                print("stop charge")
                utc_time = get_utc()
                # start transaction
                await websocket.send(json.dumps(
                    [2, id,"StopTransaction",{"transactionId":12,"idTag":"1234","timestamp":utc_time,"meterStop":2}]
                ))
                response = await websocket.recv()
                print(response)
            
            if x  == 'h':
                print("get heartbeat")
                await websocket.send(json.dumps(
                    [2,id,"Heartbeat",{}]
                ))
                response = await websocket.recv()
                print(response)
            
            if x == 'c':
                # simulate charging for 1 minute

                charging_time = 60
                starting_meter = 0
                curr = time.time()
                while time.time() < curr + charging_time:

                    starting_meter += round(math.pi, 4)
                    time.sleep(5)




        # stop transactrion

def get_utc():
    now_utc = datetime.now(timezone.utc)
    return now_utc
if __name__ == '__main__':
    #asyncio.get_event_loop().run_until_complete(run())
    asyncio.run(run())